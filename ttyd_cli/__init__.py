"""
TTYD Over Terminal Client
A cross-platform terminal client for ttyd websocket connections.
"""

from .client import TTYDClient
from .exceptions import InvalidAuthorization

__all__ = ["TTYDClient", "InvalidAuthorization"]
