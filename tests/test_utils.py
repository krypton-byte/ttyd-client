"""
Tests for utility functions.
"""

import unittest
from unittest.mock import Mock, patch

from ttyd_cli.utils import get_terminal_size


class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""

    @patch("ttyd_cli.utils.IS_WINDOWS", False)
    @patch("os.get_terminal_size")
    def test_get_terminal_size_unix(self, mock_get_size):
        """Test getting terminal size on Unix."""
        mock_size = Mock()
        mock_size.columns = 100
        mock_size.lines = 30
        mock_get_size.return_value = mock_size

        cols, rows = get_terminal_size()
        self.assertEqual(cols, 100)
        self.assertEqual(rows, 30)

    @patch("ttyd_cli.utils.IS_WINDOWS", True)
    @patch("os.get_terminal_size")
    def test_get_terminal_size_windows(self, mock_get_size):
        """Test getting terminal size on Windows."""
        mock_size = Mock()
        mock_size.columns = 120
        mock_size.lines = 40
        mock_get_size.return_value = mock_size

        cols, rows = get_terminal_size()
        self.assertEqual(cols, 120)
        self.assertEqual(rows, 40)

    @patch("os.get_terminal_size")
    def test_get_terminal_size_fallback(self, mock_get_size):
        """Test terminal size fallback on error."""
        mock_get_size.side_effect = OSError("Not a terminal")

        cols, rows = get_terminal_size()
        # Should return default values
        self.assertIsInstance(cols, int)
        self.assertIsInstance(rows, int)
        self.assertGreater(cols, 0)
        self.assertGreater(rows, 0)


if __name__ == "__main__":
    unittest.main()
