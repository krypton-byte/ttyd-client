"""
TTYD WebSocket client implementation.
"""

from __future__ import annotations

import re
import sys
import time
from sys import stdout
from threading import Thread
from urllib.parse import quote

import websocket

from .auth import authenticate
from .platforms import InputHandler
from .utils import IS_WINDOWS, get_terminal_size

if not IS_WINDOWS:
    from signal import SIGWINCH, signal


class TTYDClient(websocket.WebSocketApp):
    """
    WebSocket client for TTYD terminal connections.
    """

    # Regex patterns for terminal query sequences that should be filtered
    QUERY_PATTERNS = [
        rb"\x1b\]10;[^\x07\x1b]*(?:\x07|\x1b\\)",  # Foreground color query
        rb"\x1b\]11;[^\x07\x1b]*(?:\x07|\x1b\\)",  # Background color query
        rb"\x1b\]12;[^\x07\x1b]*(?:\x07|\x1b\\)",  # Cursor color query
        rb"\x1b\]4;[^\x07\x1b]*(?:\x07|\x1b\\)",  # Color palette query
        rb"\x1b\[>\d*[cq]",  # Device attributes query
        rb"\x1b\[\?[0-9;]*c",  # Primary DA query
        rb"\x1b\[=\d*c",  # Secondary DA query
        rb"\x1bP[^\x1b]*\x1b\\",  # DCS sequences
        rb"\x1b_[^\x1b]*\x1b\\",  # APC sequences
    ]

    def __init__(
        self,
        url: str,
        credential: str | None = None,
        args: list[str] = [],
        cmd: str = "",
        verify: bool = True,
    ) -> None:
        """
        Initialize TTYD client.

        Args:
            url: Base URL of TTYD server (http/https)
            credential: Optional authentication in format "username:password"
            args: Command line arguments to pass to remote shell
            cmd: Command to execute on connection
            verify: Whether to verify SSL certificates

        Raises:
            InvalidAuthorization: If authentication fails
        """
        # Authenticate and get token
        token = authenticate(url, credential, verify)

        # Build WebSocket URL
        ws_url = "ws" + url[4:] + "/ws?" + "".join([f"arg={quote(x)}" for x in args])
        headers = [
            "Sec-WebSocket-Protocol: tty",
            f"Authorization: Basic {token}" if token else "Authorization: Basic ",
        ]

        super().__init__(
            ws_url,
            header=headers,
            on_open=self._on_open,
            on_message=self._on_message,
            on_close=self._on_close,
        )

        self.credential: str | None = token
        self.cmd: str = cmd
        self.connected: bool = False
        self._connection_established: bool = False
        self._input_handler: InputHandler | None = None

        # Compile regex patterns for performance
        self._query_regex = re.compile(b"|".join(self.QUERY_PATTERNS))

        # Windows resize monitoring
        if IS_WINDOWS:
            self._last_size: tuple | None = None
            self._resize_monitor_running: bool = False

    def _filter_output(self, data: bytes) -> bytes:
        """
        Filter out terminal query sequences from server output.

        These queries would cause the local terminal to send responses,
        which would then be read as keyboard input and sent back to server.

        Args:
            data: Raw output data from server

        Returns:
            bytes: Filtered output data
        """
        # Remove all query sequences
        filtered = self._query_regex.sub(b"", data)
        return filtered

    def _on_close(self, ws: websocket.WebSocketApp, code: int, msg: str) -> None:
        """
        Handle WebSocket close event.

        Args:
            ws: WebSocket instance
            code: Close status code
            msg: Close message
        """
        if not self._connection_established:
            print("connection refused")

        if self._input_handler:
            self._input_handler.restore_terminal()
            self._input_handler.stop()

        # Stop Windows resize monitor
        if IS_WINDOWS:
            self._resize_monitor_running = False

        self.connected = False

    def _on_message(self, ws: websocket.WebSocketApp, msg: bytes) -> None:
        """
        Handle incoming WebSocket messages.

        Args:
            ws: WebSocket instance
            msg: Message payload
        """
        if not self.connected:
            self.connected = True
            self._connection_established = True

            if self.cmd:
                self._send_command(self.cmd + "\n")

            # Start input handler thread
            self._input_handler = InputHandler(self._send_command)
            thread = Thread(target=self._input_handler.run)
            thread.daemon = True
            thread.start()

        # Message type 0 = output
        if msg[0] == 48:
            # Filter the output before writing to stdout
            filtered_output = self._filter_output(msg[1:])
            if filtered_output:  # Only write if there's something left after filtering
                stdout.write(filtered_output.decode(errors="replace"))
                stdout.flush()

    def _resize(self, *args) -> None:
        """
        Handle terminal resize event.

        Args:
            *args: Signal handler arguments (unused)
        """
        cols, rows = get_terminal_size()
        self.send('1{"columns":%s,"rows":%s}' % (cols, rows))

    def _send_command(self, c: str) -> None:
        """
        Send command to remote terminal.

        Args:
            c: Command string to send
        """
        if not self.connected:
            if self._input_handler:
                self._input_handler.restore_terminal()
            sys.exit(0 if self._connection_established else 1)

        # Convert newline to carriage return for terminal
        self.send("0" + ("\r" if c == "\n" else c))

    def _start_windows_resize_monitor(self) -> None:
        """
        Start monitoring terminal size changes on Windows.
        Runs in a separate thread and polls for size changes.
        """
        if not IS_WINDOWS:
            return

        def monitor_resize():
            self._resize_monitor_running = True
            self._last_size = get_terminal_size()

            while self._resize_monitor_running and self.connected:
                try:
                    current_size = get_terminal_size()
                    if current_size != self._last_size:
                        self._last_size = current_size
                        self._resize()
                    time.sleep(0.5)  # Check every 500ms
                except Exception:
                    pass

        thread = Thread(target=monitor_resize)
        thread.daemon = True
        thread.start()

    def _on_open(self, ws: websocket.WebSocketApp) -> None:
        """
        Handle WebSocket open event.

        Args:
            ws: WebSocket instance
        """
        # Send authentication token
        self.send('{"AuthToken":"%s"}' % (self.credential or ""))

        # Setup window resize signal (Unix only)
        if not IS_WINDOWS:
            try:
                signal(SIGWINCH, self._resize)
            except Exception:
                pass
        else:
            # Start resize monitoring for Windows
            self._start_windows_resize_monitor()

        # Send initial terminal size
        self._resize()
