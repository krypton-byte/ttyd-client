"""
TTYD Over Terminal Client
A cross-platform terminal client for ttyd websocket connections.
"""

from importlib.metadata import PackageNotFoundError, version

from .client import TTYDClient
from .exceptions import InvalidAuthorization

__version__ = "0.1.0"

__all__ = ["TTYDClient", "InvalidAuthorization"]
