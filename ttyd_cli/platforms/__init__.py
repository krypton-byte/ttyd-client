"""
Platform-specific terminal input handlers.
"""

from ..utils import IS_WINDOWS
from .base import TerminalInputHandler

if IS_WINDOWS:
    from .windows import WindowsInputHandler as InputHandler
else:
    from .unix import UnixInputHandler as InputHandler

__all__ = ["TerminalInputHandler", "InputHandler"]
