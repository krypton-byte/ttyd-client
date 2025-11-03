"""
Tests for custom exceptions.
"""

import unittest

from ttyd_cli.exceptions import InvalidAuthorization


class TestExceptions(unittest.TestCase):
    """Test cases for custom exceptions."""

    def test_invalid_authorization_message(self):
        """Test InvalidAuthorization exception message."""
        msg = "Authentication failed"
        exc = InvalidAuthorization(msg)
        self.assertEqual(str(exc), msg)

    def test_invalid_authorization_inheritance(self):
        """Test InvalidAuthorization inherits from Exception."""
        exc = InvalidAuthorization("test")
        self.assertIsInstance(exc, Exception)

    def test_invalid_authorization_raise(self):
        """Test raising InvalidAuthorization."""
        with self.assertRaises(InvalidAuthorization) as cm:
            raise InvalidAuthorization("Test error")
        self.assertEqual(str(cm.exception), "Test error")


if __name__ == "__main__":
    unittest.main()
