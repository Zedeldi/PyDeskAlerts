"""Start web interface for the DeskAlerts network."""

import socket
import sys
from typing import NoReturn

from deskalerts.server import app


def main() -> NoReturn:
    """Start the server Flask application."""
    try:
        HOST = str(sys.argv[1])
        PORT = int(sys.argv[2])
        if PORT < 0 or PORT > 65535:
            raise ValueError
    except (IndexError, ValueError):
        HOST = "0.0.0.0"
        PORT = 8080
    try:
        app.run(HOST, PORT)
    except socket.error as e:
        print(f"Failed to bind: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        sys.exit(0)


if __name__ == "__main__":
    main()
