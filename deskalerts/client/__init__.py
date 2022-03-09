"""Client application for the DeskAlerts network."""

import os
from pathlib import Path
from threading import Timer
from typing import NoReturn

import requests
from plyer import notification


class Client:
    def __init__(self, host: str, port: int, interval: int = 300) -> None:
        """
        Initialise client.

        interval is the number of seconds to check for new messages.
        """
        self.interval = interval
        self._server = f"http://{host}:{port}"
        self._icon = Path(__file__).absolute().parent / "icon.ico"

    def check_for_updates(self) -> list[str]:
        """Return new messages from the server."""
        response = requests.get(f"{self._server}/get?user={os.getlogin()}").json()
        return response["messages"]

    def display_messages(self) -> None:
        """Handle displaying new messages and scheduling next update."""
        messages = self.check_for_updates()
        for message in messages:
            notification.notify(
                title="New Alert",
                message=message,
                app_name="DeskAlerts",
                app_icon=str(self._icon),
            )
        self._schedule_update()

    def _schedule_update(self) -> None:
        """Start a timer to check for updates after configured interval."""
        t = Timer(self.interval, self.display_messages)
        t.start()

    def run(self) -> NoReturn:
        """Periodically check for updates."""
        self._schedule_update()
