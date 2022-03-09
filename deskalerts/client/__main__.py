"""Start client application for the DeskAlerts network."""

import sys
from typing import NoReturn

from deskalerts.client import Client


def main() -> NoReturn:
    """Start the server Flask application."""
    try:
        HOST = str(sys.argv[1])
        PORT = int(sys.argv[2])
        if PORT < 0 or PORT > 65535:
            raise ValueError
    except (IndexError, ValueError):
        HOST = "127.0.0.1"
        PORT = 8080

    client = Client(HOST, PORT)
    try:
        client.run()
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        sys.exit(0)


if __name__ == "__main__":
    main()
