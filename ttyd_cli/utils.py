"""
Utility functions for terminal operations.
"""

import platform
from typing import Tuple

IS_WINDOWS: bool = platform.system() == 'Windows'


def get_terminal_size() -> Tuple[int, int]:
    """
    Get terminal size in a cross-platform way.
    
    Returns:
        Tuple[int, int]: (columns, rows) of the terminal
    """
    if IS_WINDOWS:
        try:
            from shutil import get_terminal_size as shutil_get_size
            size = shutil_get_size()
            return (size.columns, size.rows)
        except Exception:
            return (80, 24)  # Default fallback
    else:
        try:
            from os import get_terminal_size as os_get_terminal_size
            size = os_get_terminal_size()
            return (size.columns, size.lines)
        except Exception:
            return (80, 24)
