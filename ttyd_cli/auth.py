"""
Authentication and web session handling.
"""

import base64

from requests import Session

from .exceptions import InvalidAuthorization


class WebPage(Session):
    """
    HTTP session handler for TTYD authentication.
    """

    def __init__(self, url: str, verify: bool = True) -> None:
        """
        Initialize web session.

        Args:
            url: Base URL of the TTYD server
            verify: Whether to verify SSL certificates
        """
        super().__init__()
        self.verify: bool = verify
        self.url: str = url

    def token(self, username: str, password: str) -> str:
        """
        Retrieve authentication token using basic auth.

        Args:
            username: Username for authentication
            password: Password for authentication

        Returns:
            str: Authentication token

        Raises:
            InvalidAuthorization: If credentials are invalid
        """
        b = base64.b64encode(f"{username}:{password}".encode()).decode()
        self.headers["Authorization"] = f"Basic {b}"
        response = self.get(self.url + "/token", verify=self.verify)

        if response.status_code == 200:
            return response.json()["token"]

        raise InvalidAuthorization("Credential Invalid")

    def check(self) -> None:
        """
        Check if server is accessible.

        Raises:
            InvalidAuthorization: If server is not accessible
        """
        if self.get(self.url, verify=self.verify).status_code != 200:
            raise InvalidAuthorization("Server not accessible")


def authenticate(url: str, credential: str | None = None, verify: bool = True) -> str | None:
    """
    Authenticate with TTYD server and get token.

    Args:
        url: Base URL of the TTYD server
        credential: Optional credentials in format "username:password"
        verify: Whether to verify SSL certificates

    Returns:
        Optional[str]: Authentication token or None if no auth required

    Raises:
        InvalidAuthorization: If authentication fails
    """
    page = WebPage(url, verify)

    try:
        page.check()
        return None  # No authentication required
    except InvalidAuthorization:
        if credential:
            username, password = credential.split(":", 1)
            return page.token(username, password)
        else:
            raise InvalidAuthorization("Credential Required")
