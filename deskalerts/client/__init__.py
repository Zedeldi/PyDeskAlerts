"""Client application for the DeskAlerts network."""

import os
from pathlib import Path
from threading import Timer
from typing import Any

import requests
from plyer import notification


class Client:
    """Client application for DeskAlerts."""

    def __init__(self, host: str, port: int, interval: int = 300) -> None:
        """
        Initialise client.

        interval is the number of seconds to check for new alerts.
        """
        self.interval = interval
        self._server = f"http://{host}:{port}"
        self._icon = Path(__file__).absolute().parent / "icon.ico"

    def check_for_updates(self) -> list[dict[str, Any]]:
        """Return new alerts from the server."""
        response = requests.get(f"{self._server}/get?user={os.getlogin()}").json()
        return response["alerts"]

    def display_alerts(self) -> None:
        """Handle displaying new alerts and scheduling next update."""
        alerts = self.check_for_updates()
        for alert in alerts:
            notification.notify(
                title="New Alert",
                message=alert["message"],
                app_name="DeskAlerts",
                app_icon=str(self._icon),
            )
        self._schedule_update()

    def _schedule_update(self) -> None:
        """Start a timer to check for updates after configured interval."""
        t = Timer(self.interval, self.display_alerts)
        t.start()

    def run(self) -> None:
        """Periodically check for updates."""
        self._schedule_update()
