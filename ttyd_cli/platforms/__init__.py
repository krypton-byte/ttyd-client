"""
Platform-specific terminal input handlers.
"""

from .base import TerminalInputHandler
from ..utils import IS_WINDOWS

if IS_WINDOWS:
    from .windows import WindowsInputHandler as InputHandler
else:
    from .unix import UnixInputHandler as InputHandler

__all__ = ["TerminalInputHandler", "InputHandler"]
