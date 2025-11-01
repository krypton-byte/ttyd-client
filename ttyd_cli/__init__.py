"""
TTYD Over Terminal Client
A cross-platform terminal client for ttyd websocket connections.
"""

from .client import TTYDClient
from .exceptions import InvalidAuthorization

__version__ = "1.0.0"
__all__ = ["TTYDClient", "InvalidAuthorization"]
