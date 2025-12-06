"""
Tests for Unix input handler.
"""

import sys
import unittest
from unittest.mock import Mock, patch

# Only run these tests on Unix-like systems
if sys.platform != "win32":
    from ttyd_cli.platforms.unix import UnixInputHandler


class TestUnixInputHandler(unittest.TestCase):
    """Test cases for UnixInputHandler."""

    def setUp(self):
        """Set up test handler."""
        if sys.platform == "win32":
            self.skipTest("Unix-specific tests")
        self.send_callback = Mock()

    @patch("sys.stdin")
    @patch("select.select")
    @patch("termios.tcgetattr")
    def test_arrow_up_key(self, mock_tcgetattr, mock_select, mock_stdin):
        """Test arrow up key sends complete escape sequence."""
        # Mock termios
        mock_tcgetattr.return_value = []

        # Create handler
        handler = UnixInputHandler(self.send_callback)

        # Simulate arrow up key: ESC [ A
        mock_stdin.read = Mock(side_effect=["\x1b", "[", "A"])
        # select returns True for first two calls (more data available)
        mock_select.side_effect = [[True], [True], [False]]

        result = handler.read_input()

        # Should return complete escape sequence
        self.assertEqual(result, "\x1b[A")

    @patch("sys.stdin")
    @patch("select.select")
    @patch("termios.tcgetattr")
    def test_arrow_down_key(self, mock_tcgetattr, mock_select, mock_stdin):
        """Test arrow down key sends complete escape sequence."""
        mock_tcgetattr.return_value = []
        handler = UnixInputHandler(self.send_callback)

        # Simulate arrow down key: ESC [ B
        mock_stdin.read = Mock(side_effect=["\x1b", "[", "B"])
        mock_select.side_effect = [[True], [True], [False]]

        result = handler.read_input()
        self.assertEqual(result, "\x1b[B")

    @patch("sys.stdin")
    @patch("select.select")
    @patch("termios.tcgetattr")
    def test_arrow_right_key(self, mock_tcgetattr, mock_select, mock_stdin):
        """Test arrow right key sends complete escape sequence."""
        mock_tcgetattr.return_value = []
        handler = UnixInputHandler(self.send_callback)

        # Simulate arrow right key: ESC [ C
        mock_stdin.read = Mock(side_effect=["\x1b", "[", "C"])
        mock_select.side_effect = [[True], [True], [False]]

        result = handler.read_input()
        self.assertEqual(result, "\x1b[C")

    @patch("sys.stdin")
    @patch("select.select")
    @patch("termios.tcgetattr")
    def test_arrow_left_key(self, mock_tcgetattr, mock_select, mock_stdin):
        """Test arrow left key sends complete escape sequence."""
        mock_tcgetattr.return_value = []
        handler = UnixInputHandler(self.send_callback)

        # Simulate arrow left key: ESC [ D
        mock_stdin.read = Mock(side_effect=["\x1b", "[", "D"])
        mock_select.side_effect = [[True], [True], [False]]

        result = handler.read_input()
        self.assertEqual(result, "\x1b[D")

    @patch("sys.stdin")
    @patch("select.select")
    @patch("termios.tcgetattr")
    def test_escape_key_alone(self, mock_tcgetattr, mock_select, mock_stdin):
        """Test ESC key alone (no following sequence)."""
        mock_tcgetattr.return_value = []
        handler = UnixInputHandler(self.send_callback)

        # Simulate ESC key alone - no more data after timeout
        mock_stdin.read = Mock(return_value="\x1b")
        mock_select.return_value = ([], [], [])  # No more data available

        result = handler.read_input()
        self.assertEqual(result, "\x1b")

    @patch("sys.stdin")
    @patch("select.select")
    @patch("termios.tcgetattr")
    def test_function_key_f1(self, mock_tcgetattr, mock_select, mock_stdin):
        """Test F1 key sends complete escape sequence."""
        mock_tcgetattr.return_value = []
        handler = UnixInputHandler(self.send_callback)

        # Simulate F1 key: ESC O P
        mock_stdin.read = Mock(side_effect=["\x1b", "O", "P"])
        mock_select.side_effect = [[True], [True]]

        result = handler.read_input()
        self.assertEqual(result, "\x1bOP")

    @patch("sys.stdin")
    @patch("select.select")
    @patch("termios.tcgetattr")
    def test_device_control_sequence_filtered(self, mock_tcgetattr, mock_select, mock_stdin):
        """Test device control sequences are filtered out."""
        mock_tcgetattr.return_value = []
        handler = UnixInputHandler(self.send_callback)

        # Simulate cursor position report: ESC [ 1 ; 1 R
        mock_stdin.read = Mock(side_effect=["\x1b", "[", "1", ";", "1", "R"])
        mock_select.side_effect = [[True], [True], [True], [True], [True], [False]]

        result = handler.read_input()
        # Should be filtered out (return None)
        self.assertIsNone(result)

    @patch("sys.stdin")
    @patch("select.select")
    @patch("termios.tcgetattr")
    def test_regular_character(self, mock_tcgetattr, mock_select, mock_stdin):
        """Test regular character is passed through."""
        mock_tcgetattr.return_value = []
        handler = UnixInputHandler(self.send_callback)

        mock_stdin.read = Mock(return_value="a")

        result = handler.read_input()
        self.assertEqual(result, "a")

    @patch("sys.stdin")
    @patch("select.select")
    @patch("termios.tcgetattr")
    def test_page_up_key(self, mock_tcgetattr, mock_select, mock_stdin):
        """Test Page Up key sends complete escape sequence."""
        mock_tcgetattr.return_value = []
        handler = UnixInputHandler(self.send_callback)

        # Simulate Page Up key: ESC [ 5 ~
        mock_stdin.read = Mock(side_effect=["\x1b", "[", "5", "~"])
        mock_select.side_effect = [[True], [True], [True], [False]]

        result = handler.read_input()
        self.assertEqual(result, "\x1b[5~")

    @patch("sys.stdin")
    @patch("select.select")
    @patch("termios.tcgetattr")
    def test_home_key(self, mock_tcgetattr, mock_select, mock_stdin):
        """Test Home key sends complete escape sequence."""
        mock_tcgetattr.return_value = []
        handler = UnixInputHandler(self.send_callback)

        # Simulate Home key: ESC [ H
        mock_stdin.read = Mock(side_effect=["\x1b", "[", "H"])
        mock_select.side_effect = [[True], [True], [False]]

        result = handler.read_input()
        self.assertEqual(result, "\x1b[H")


if __name__ == "__main__":
    unittest.main()
