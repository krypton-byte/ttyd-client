"""
Tests for TTYD WebSocket client.
"""

import unittest
from unittest.mock import Mock, patch

from ttyd_cli.client import TTYDClient


class TestTTYDClient(unittest.TestCase):
    """Test cases for TTYDClient."""

    @patch("ttyd_cli.client.authenticate")
    def setUp(self, mock_auth):
        """Set up test client."""
        mock_auth.return_value = "test_token"
        self.client = TTYDClient(url="http://localhost:7681", credential="user:pass", verify=False)

    def test_client_initialization(self):
        """Test client initialization."""
        self.assertEqual(self.client.credential, "test_token")
        self.assertEqual(self.client.cmd, "")
        self.assertFalse(self.client.connected)
        self.assertFalse(self.client._connection_established)

    def test_filter_output_foreground_color(self):
        """Test filtering foreground color query."""
        data = b"\x1b]10;rgb:0000/0000/0000\x07Hello"
        filtered = self.client._filter_output(data)
        self.assertEqual(filtered, b"Hello")

    def test_filter_output_background_color(self):
        """Test filtering background color query."""
        data = b"\x1b]11;rgb:ffff/ffff/ffff\x07World"
        filtered = self.client._filter_output(data)
        self.assertEqual(filtered, b"World")

    def test_filter_output_device_attributes(self):
        """Test filtering device attributes query."""
        data = b"\x1b[>0cTest"
        filtered = self.client._filter_output(data)
        self.assertEqual(filtered, b"Test")

    def test_filter_output_primary_da(self):
        """Test filtering primary DA query."""
        data = b"\x1b[?1;2cData"
        filtered = self.client._filter_output(data)
        self.assertEqual(filtered, b"Data")

    def test_filter_output_dcs_sequence(self):
        """Test filtering DCS sequences."""
        data = b"\x1bPtest\x1b\\Content"
        filtered = self.client._filter_output(data)
        self.assertEqual(filtered, b"Content")

    def test_filter_output_multiple_queries(self):
        """Test filtering multiple query sequences."""
        data = b"\x1b]10;rgb:0000/0000/0000\x07\x1b[>0cHello\x1b]11;rgb:ffff/ffff/ffff\x07"
        filtered = self.client._filter_output(data)
        self.assertEqual(filtered, b"Hello")

    def test_filter_output_no_queries(self):
        """Test output without query sequences."""
        data = b"Plain text output"
        filtered = self.client._filter_output(data)
        self.assertEqual(filtered, data)

    def test_on_close_not_connected(self):
        """Test on_close when not connected."""
        mock_ws = Mock()
        with patch("builtins.print") as mock_print:
            self.client._on_close(mock_ws, 1000, "Normal")
            mock_print.assert_called_once_with("connection refused")

    def test_on_close_with_input_handler(self):
        """Test on_close with input handler."""
        mock_ws = Mock()
        mock_handler = Mock()
        self.client._connection_established = True
        self.client._input_handler = mock_handler

        self.client._on_close(mock_ws, 1000, "Normal")

        mock_handler.restore_terminal.assert_called_once()
        mock_handler.stop.assert_called_once()
        self.assertFalse(self.client.connected)

    @patch("ttyd_cli.client.get_terminal_size")
    def test_resize(self, mock_size):
        """Test terminal resize."""
        mock_size.return_value = (80, 24)
        with patch.object(self.client, "send") as mock_send:
            self.client._resize()
            mock_send.assert_called_once_with('1{"columns":80,"rows":24}')

    def test_send_command_newline(self):
        """Test sending newline command."""
        self.client.connected = True
        with patch.object(self.client, "send") as mock_send:
            self.client._send_command("\n")
            mock_send.assert_called_once_with("0\r")

    def test_send_command_regular_char(self):
        """Test sending regular character."""
        self.client.connected = True
        with patch.object(self.client, "send") as mock_send:
            self.client._send_command("a")
            mock_send.assert_called_once_with("0a")

    def test_send_command_not_connected(self):
        """Test sending command when not connected."""
        self.client.connected = False
        self.client._connection_established = True
        with self.assertRaises(SystemExit) as cm:
            self.client._send_command("test")
        self.assertEqual(cm.exception.code, 0)

    def test_on_message_output(self):
        """Test handling output message."""
        self.client.connected = True
        mock_ws = Mock()
        msg = b"0Hello World"

        with patch("sys.stdout") as mock_stdout:
            self.client._on_message(mock_ws, msg)
            mock_stdout.write.assert_called()

    @patch("ttyd_cli.client.Thread")
    @patch("ttyd_cli.client.InputHandler")
    def test_on_message_first_connection(self, mock_handler_class, mock_thread):
        """Test first message after connection."""
        mock_ws = Mock()
        msg = b"0"
        self.client.cmd = "ls"

        with patch.object(self.client, "_send_command") as mock_send:
            self.client._on_message(mock_ws, msg)
            mock_send.assert_called_with("ls\n")
            self.assertTrue(self.client.connected)
            self.assertTrue(self.client._connection_established)

    @patch("ttyd_cli.client.get_terminal_size")
    def test_on_open(self, mock_size):
        """Test WebSocket open event."""
        mock_ws = Mock()
        mock_size.return_value = (80, 24)

        with patch.object(self.client, "send") as mock_send:
            self.client._on_open(mock_ws)
            # Should send auth token and terminal size
            self.assertEqual(mock_send.call_count, 2)


class TestTTYDClientWindows(unittest.TestCase):
    """Test cases for Windows-specific functionality."""

    @patch("ttyd_cli.client.IS_WINDOWS", True)
    @patch("ttyd_cli.client.authenticate")
    def test_windows_resize_monitor_initialization(self, mock_auth):
        """Test Windows resize monitor initialization."""
        mock_auth.return_value = "test_token"
        client = TTYDClient(url="http://localhost:7681")
        self.assertIsNone(client._last_size)
        self.assertFalse(client._resize_monitor_running)


if __name__ == "__main__":
    unittest.main()
