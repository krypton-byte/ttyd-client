"""
Tests for authentication module.
"""

import unittest
from unittest.mock import Mock, patch

from ttyd_cli.auth import authenticate
from ttyd_cli.exceptions import InvalidAuthorization

url = "http://localhost:7681"


class TestAuthentication(unittest.TestCase):
    """Test cases for authentication."""

    @patch("ttyd_cli.auth.requests.get")
    def test_authenticate_no_credential(self, mock_get):
        """Test authentication without credentials."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        token = authenticate("url", None, True)
        self.assertIsNone(token)

    @patch("ttyd_cli.auth.requests.get")
    def test_authenticate_with_credential(self, mock_get):
        """Test authentication with credentials."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        token = authenticate("url", "user:pass", True)
        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)

    @patch("ttyd_cli.auth.requests.get")
    def test_authenticate_invalid_credentials(self, mock_get):
        """Test authentication with invalid credentials."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        with self.assertRaises(InvalidAuthorization):
            authenticate("url", "wrong:creds", True)

    @patch("ttyd_cli.auth.requests.get")
    def test_authenticate_server_error(self, mock_get):
        """Test authentication with server error."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        with self.assertRaises(InvalidAuthorization):
            authenticate("url", "user:pass", True)

    @patch("ttyd_cli.auth.requests.get")
    def test_authenticate_no_verify_ssl(self, mock_get):
        """Test authentication with SSL verification disabled."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        authenticate("https://localhost:7681", None, False)
        mock_get.assert_called_once()
        self.assertFalse(mock_get.call_args[1]["verify"])


if __name__ == "__main__":
    unittest.main()
