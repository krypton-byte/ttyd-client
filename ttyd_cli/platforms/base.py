"""
Base class for platform-specific input handlers.
"""

from abc import ABC, abstractmethod
from collections.abc import Callable


class TerminalInputHandler(ABC):
    """
    Abstract base class for terminal input handling.
    """

    def __init__(self, send_callback: Callable[[str], None]) -> None:
        """
        Initialize input handler.

        Args:
            send_callback: Function to call when sending input to remote
        """
        self.send_callback: Callable[[str], None] = send_callback
        self.connected: bool = True

    @abstractmethod
    def read_input(self) -> str | None:
        """
        Read a single input from terminal.

        Returns:
            Optional[str]: The input character(s) or escape sequence
        """
        pass

    @abstractmethod
    def run(self) -> None:
        """
        Main input loop.
        """
        pass

    @abstractmethod
    def restore_terminal(self) -> None:
        """
        Restore terminal to original state.
        """
        pass

    def stop(self) -> None:
        """
        Signal the input handler to stop.
        """
        self.connected = False
