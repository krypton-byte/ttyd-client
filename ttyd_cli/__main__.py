"""
Command-line interface for TTYD client.
"""

import argparse
import sys

from .client import TTYDClient
from .exceptions import InvalidAuthorization


def main() -> None:
    """
    Main entry point for CLI.
    """
    parser = argparse.ArgumentParser(
        description="TTYD WebSocket Terminal Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--url",
        type=str,
        required=True,
        help="TTYD server URL (e.g., http://example.com:7681)",
    )
    parser.add_argument(
        "--no-verify", action="store_true", help="Disable SSL certificate verification"
    )
    parser.add_argument(
        "--credential",
        type=str,
        help='Authentication credentials in format "username:password"',
    )
    parser.add_argument(
        "args",
        metavar="ARGS",
        nargs="*",
        default=[],
        help="Arguments to pass to remote shell",
    )
    parser.add_argument("-c", type=str, default="", help="Command to execute on connection")

    args = parser.parse_args()

    try:
        # Create and run client
        client = TTYDClient(
            url=args.url,
            credential=args.credential,
            args=args.args,
            cmd=args.c,
            verify=not args.no_verify,
        )
        client.run_forever()

    except InvalidAuthorization as e:
        sys.stderr.write(f"[*] {str(e)}\n")
        sys.stderr.flush()
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        sys.stderr.write(f"[!] Error: {str(e)}\n")
        sys.stderr.flush()
        sys.exit(1)


if __name__ == "__main__":
    main()
