"""
TTYD Over Terminal Client
A cross-platform terminal client for ttyd websocket connections.
"""

from importlib.metadata import PackageNotFoundError, version

from .client import TTYDClient
from .exceptions import InvalidAuthorization

try:
    __version__ = version("ttyd-client")
except PackageNotFoundError:
    __version__ = "0.0.0.dev0"

__all__ = ["TTYDClient", "InvalidAuthorization"]
