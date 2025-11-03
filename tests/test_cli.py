"""
Tests for CLI module.
"""

import unittest
from unittest.mock import Mock, patch

from ttyd_cli.cli import main
from ttyd_cli.exceptions import InvalidAuthorization


class TestCLI(unittest.TestCase):
    """Test cases for CLI."""

    @patch("ttyd_cli.cli.TTYDClient")
    @patch("sys.argv", ["ttyd-client", "http://localhost:7681"])
    def test_main_basic(self, mock_client_class):
        """Test basic CLI invocation."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        main()

        mock_client_class.assert_called_once()
        mock_client.run_forever.assert_called_once()

    @patch("ttyd_cli.cli.TTYDClient")
    @patch("sys.argv", ["ttyd-client", "http://localhost:7681", "-c", "user:pass"])
    def test_main_with_credential(self, mock_client_class):
        """Test CLI with credentials."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        main()

        args = mock_client_class.call_args[1]
        self.assertEqual(args["credential"], "user:pass")

    @patch("ttyd_cli.cli.TTYDClient")
    @patch("sys.argv", ["ttyd-client", "http://localhost:7681", "--cmd", "ls -la"])
    def test_main_with_command(self, mock_client_class):
        """Test CLI with command."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        main()

        args = mock_client_class.call_args[1]
        self.assertEqual(args["cmd"], "ls -la")

    @patch("ttyd_cli.cli.TTYDClient")
    @patch("sys.argv", ["ttyd-client", "http://localhost:7681", "--no-verify"])
    def test_main_no_verify(self, mock_client_class):
        """Test CLI with SSL verification disabled."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        main()

        args = mock_client_class.call_args[1]
        self.assertFalse(args["verify"])

    @patch("ttyd_cli.cli.TTYDClient")
    @patch("sys.argv", ["ttyd-client", "http://localhost:7681", "-a", "bash", "--login"])
    def test_main_with_args(self, mock_client_class):
        """Test CLI with shell arguments."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        main()

        args = mock_client_class.call_args[1]
        self.assertEqual(args["args"], ["bash", "--login"])

    @patch("ttyd_cli.cli.TTYDClient")
    @patch("sys.argv", ["ttyd-client", "http://localhost:7681"])
    def test_main_invalid_auth(self, mock_client_class):
        """Test CLI with authentication failure."""
        mock_client_class.side_effect = InvalidAuthorization("Invalid credentials")

        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)

    @patch("ttyd_cli.cli.TTYDClient")
    @patch("sys.argv", ["ttyd-client", "http://localhost:7681"])
    def test_main_keyboard_interrupt(self, mock_client_class):
        """Test CLI with keyboard interrupt."""
        mock_client = Mock()
        mock_client.run_forever.side_effect = KeyboardInterrupt()
        mock_client_class.return_value = mock_client

        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)

    @patch("sys.argv", ["ttyd-client", "--version"])
    def test_main_version(self):
        """Test CLI version display."""
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
