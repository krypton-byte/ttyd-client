"""
Unix/Linux/macOS terminal input handler.
"""

import select
import sys
import termios
import tty
from collections.abc import Callable

from .base import TerminalInputHandler


class UnixInputHandler(TerminalInputHandler):
    """
    Terminal input handler for Unix-like systems.
    """

    def __init__(self, send_callback: Callable[[str], None]) -> None:
        """
        Initialize Unix input handler.

        Args:
            send_callback: Function to call when sending input to remote
        """
        super().__init__(send_callback)
        self.original_attrs: list | None = None

        try:
            self.original_attrs = termios.tcgetattr(sys.stdin.fileno())
        except Exception:
            self.original_attrs = None

    def _is_device_control_sequence(self, sequence: str) -> bool:
        """
        Check if sequence is a device control/response that should be ignored.

        These are terminal responses to queries, not user input.

        Args:
            sequence: The escape sequence to check

        Returns:
            bool: True if this is a device control sequence to ignore
        """
        if not sequence.startswith("\x1b"):
            return False

        # OSC (Operating System Command) responses - format: ESC ] ... ESC \ or BEL
        # Examples: color queries, window title responses
        if "\x1b]" in sequence:
            return True

        # CSI responses with specific patterns
        if sequence.startswith("\x1b["):
            # Device Status Report responses (ESC[?...$y, ESC[?...c, etc)
            if "?" in sequence and any(sequence.endswith(x) for x in ["c", "y", "R"]):
                return True

            # Primary Device Attributes response (ESC[?...c)
            if sequence.startswith("\x1b[?") and "c" in sequence:
                return True

            # Cursor position report (ESC[row;colR)
            if sequence.endswith("R") and ";" in sequence:
                try:
                    # Check if it's numeric;numeric R format
                    parts = sequence[2:-1].split(";")
                    if len(parts) == 2 and all(p.isdigit() for p in parts):
                        return True
                except Exception:
                    pass

        # DCS (Device Control String) responses - format: ESC P ... ESC \
        if sequence.startswith("\x1bP"):
            return True

        # APC (Application Program Command) - format: ESC _ ... ESC \
        if sequence.startswith("\x1b_"):
            return True

        return False

    def read_input(self) -> str | None:
        """
        Read keyboard input with escape sequence support.

        Returns:
            Optional[str]: The input character(s) or complete escape sequence,
                          or None if sequence should be ignored
        """
        ch = sys.stdin.read(1)

        # Check for escape sequences
        if ch == "\x1b":
            buffer = [ch]

            # Wait briefly to see if more characters are coming
            # Escape sequences arrive almost immediately, ESC key alone has a delay
            if select.select([sys.stdin], [], [], 0.1)[0]:
                # Read the next character
                next_ch = sys.stdin.read(1)
                buffer.append(next_ch)

                # CSI sequences start with [
                if next_ch == "[":
                    # Read until we find a terminator
                    while True:
                        if select.select([sys.stdin], [], [], 0.01)[0]:
                            ch = sys.stdin.read(1)
                            buffer.append(ch)

                            # CSI sequences end with a letter (A-Z, a-z) or ~
                            if ch.isalpha() or ch == "~":
                                break
                        else:
                            break

                # OSC sequences start with ]
                elif next_ch == "]":
                    # Read until ESC \ (ST) or BEL (\x07)
                    while True:
                        if select.select([sys.stdin], [], [], 0.01)[0]:
                            ch = sys.stdin.read(1)
                            buffer.append(ch)

                            # Check for terminator
                            if ch == "\x07":  # BEL
                                break
                            if ch == "\\" and len(buffer) >= 2 and buffer[-2] == "\x1b":  # ESC \
                                break

                            # Safety limit to prevent infinite loop
                            if len(buffer) > 1000:
                                break
                        else:
                            break

                # DCS sequences start with P
                elif next_ch == "P":
                    # Read until ESC \ (ST)
                    while True:
                        if select.select([sys.stdin], [], [], 0.01)[0]:
                            ch = sys.stdin.read(1)
                            buffer.append(ch)

                            if ch == "\\" and len(buffer) >= 2 and buffer[-2] == "\x1b":
                                break

                            if len(buffer) > 1000:
                                break
                        else:
                            break

                # APC sequences start with _
                elif next_ch == "_":
                    # Read until ESC \ (ST)
                    while True:
                        if select.select([sys.stdin], [], [], 0.01)[0]:
                            ch = sys.stdin.read(1)
                            buffer.append(ch)

                            if ch == "\\" and len(buffer) >= 2 and buffer[-2] == "\x1b":
                                break

                            if len(buffer) > 1000:
                                break
                        else:
                            break

                # OSC or other sequences starting with O
                elif next_ch == "O":
                    # Function keys like F1-F4 send \x1bOP, \x1bOQ, etc
                    if select.select([sys.stdin], [], [], 0.01)[0]:
                        ch = sys.stdin.read(1)
                        buffer.append(ch)

            sequence = "".join(buffer)

            # Filter out device control sequences
            if self._is_device_control_sequence(sequence):
                return None

            return sequence

        return ch

    def run(self) -> None:
        """
        Main input loop with raw mode enabled.
        """
        if not self.original_attrs:
            return

        old_attrs = termios.tcgetattr(sys.stdin.fileno())
        try:
            # Set raw mode - disable all input processing
            tty.setraw(sys.stdin.fileno())

            # Flush any pending input that might contain terminal responses
            # This clears the buffer before we start reading actual user input
            termios.tcflush(sys.stdin.fileno(), termios.TCIFLUSH)

            while self.connected:
                key = self.read_input()
                if key:  # Only send if not None (filtered sequences return None)
                    self.send_callback(key)
        except KeyboardInterrupt:
            # If somehow Ctrl+C reaches here, send it to remote
            self.send_callback("\x03")
        finally:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old_attrs)

    def restore_terminal(self) -> None:
        """
        Restore terminal to original state.
        """
        if self.original_attrs:
            try:
                termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, self.original_attrs)
            except Exception:
                pass
