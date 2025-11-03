"""
Utility functions for terminal operations.
"""

import platform
from typing import Tuple

IS_WINDOWS: bool = platform.system() == 'Windows'

if IS_WINDOWS:
    from shutil import get_terminal_size as _get_size
    def get_size() -> Tuple[int, int]:
        size = _get_size()
        return (size.columns, size.lines)
else:
    from os import get_terminal_size as _get_size
    def get_size() -> Tuple[int, int]:
        size = _get_size()
        return (size.columns, size.lines)

def get_terminal_size(fallback: Tuple[int, int]=(80, 24)) -> Tuple[int, int]:
    """
    Get terminal size with a fallback option.
    
    Args:
        fallback: Tuple[int, int] - Fallback size (columns, rows)

    Returns:
        Tuple[int, int]: (columns, rows) of the terminal
    """
    try:
        return get_size()
    except OSError:
        return fallback
