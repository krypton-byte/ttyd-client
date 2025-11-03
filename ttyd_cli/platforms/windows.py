"""
Windows terminal input handler.
"""

import msvcrt
import time
from collections.abc import Callable

from .base import TerminalInputHandler


class WindowsInputHandler(TerminalInputHandler):
    """
    Terminal input handler for Windows systems.
    """

    # Map Windows special keys to ANSI escape sequences
    KEY_MAP: dict[str, str] = {
        "H": "\x1b[A",  # Up arrow
        "P": "\x1b[B",  # Down arrow
        "M": "\x1b[C",  # Right arrow
        "K": "\x1b[D",  # Left arrow
        "G": "\x1b[H",  # Home
        "O": "\x1b[F",  # End
        "I": "\x1b[5~",  # Page Up
        "Q": "\x1b[6~",  # Page Down
        "R": "\x1b[2~",  # Insert
        "S": "\x1b[3~",  # Delete
        ";": "\x1b[15~",  # F1
        "<": "\x1b[16~",  # F2
        "=": "\x1b[17~",  # F3
        ">": "\x1b[18~",  # F4
        "?": "\x1b[19~",  # F5
        "@": "\x1b[20~",  # F6
        "A": "\x1b[21~",  # F7
        "B": "\x1b[23~",  # F8
        "C": "\x1b[24~",  # F9
        "D": "\x1b[25~",  # F10
    }

    def __init__(self, send_callback: Callable[[str], None]) -> None:
        """
        Initialize Windows input handler.

        Args:
            send_callback: Function to call when sending input to remote
        """
        super().__init__(send_callback)

    def read_input(self) -> str | None:
        """
        Read keyboard input with special key mapping.

        Returns:
            Optional[str]: The input character(s) or mapped escape sequence
        """
        if not msvcrt.kbhit():
            return None

        ch = msvcrt.getwch()

        # Handle special keys
        if ch in ("\x00", "\xe0"):  # Special key prefix
            ch2 = msvcrt.getwch()
            return self.KEY_MAP.get(ch2, "")

        return ch

    def run(self) -> None:
        """
        Main input loop for Windows.
        """
        while self.connected:
            if msvcrt.kbhit():
                key = self.read_input()
                if key:
                    self.send_callback(key)
            else:
                time.sleep(0.01)

    def restore_terminal(self) -> None:
        """
        Restore terminal to original state (no-op on Windows).
        """
        pass  # Windows doesn't need terminal restoration
