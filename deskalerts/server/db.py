"""Database interface and operations."""

import sqlite3
import time
from dataclasses import dataclass
from typing import Any, Optional


@dataclass(eq=True, frozen=True)
class Alert:
    """Dataclass to store information about an alert."""

    user: str
    message: str
    created: float
    expires: float
    id: Optional[int] = None


class DB:
    """Handle database operations."""

    ALL_USERS = "ALL_USERS"

    def __init__(self, database: str = "deskalerts.db") -> None:
        """Initialise database."""
        self.database = database
        self._exec_sql(
            """
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user STRING,
                message STRING,
                created REAL,
                expires REAL
            )
            """
        )
        self._exec_sql(
            """
            CREATE TABLE IF NOT EXISTS seen (
                id INTEGER,
                user STRING,
                FOREIGN KEY(id) REFERENCES alerts(id)
            )
            """
        )

    def _exec_sql(self, *args) -> list[Any]:
        """Execute SQL in database and return results."""
        conn = sqlite3.connect(self.database)
        cur = conn.cursor()
        with conn:
            res = cur.execute(*args).fetchall()
        conn.close()
        return res

    def add_alert(self, alert: Alert) -> None:
        """Add alert to database."""
        self._exec_sql(
            "INSERT INTO alerts VALUES (?, ?, ?, ?, ?)",
            (alert.id, alert.user, alert.message, alert.created, alert.expires),
        )

    def get_alerts(self, user: str) -> list[Alert]:
        """
        Return all valid alerts for the specified user and self.ALL_USERS.

        Add alert ID and user to seen table.
        """
        alerts = [
            Alert(*alert)
            for alert in self._exec_sql(
                """
                SELECT user, message, created, expires, id
                FROM alerts
                WHERE (user = (?) OR user = (?))
                AND expires > (?)
                AND id NOT IN
                (SELECT id FROM seen WHERE user = (?))
                """,
                (user, self.ALL_USERS, time.time(), user),
            )
        ]
        for alert in alerts:
            self._exec_sql("INSERT INTO seen VALUES (?, ?)", (alert.id, user))
        return alerts

    def get_messages(self, user: str) -> list[str]:
        """Return all unseen, unexpired messages for user in database."""
        return [alert.message for alert in self.get_alerts(user)]

    @property
    def alerts(self) -> list[Alert]:
        """Return list of all alerts."""
        return [
            Alert(*alert)
            for alert in self._exec_sql(
                "SELECT user, message, created, expires, id FROM alerts"
            )
        ]

    @property
    def seen_users(self) -> list[str]:
        """Return list of seen users."""
        return [user[0] for user in self._exec_sql("SELECT DISTINCT user FROM seen")]

    def get_seen_by(self, alert: Alert) -> list[str]:
        """Return list of users that have seen alert."""
        return [
            user[0]
            for user in self._exec_sql(
                "SELECT DISTINCT user FROM seen WHERE id = (?)", (alert.id,)
            )
        ]

    @property
    def seen_alerts(self) -> dict[Alert, list[str]]:
        """Return dictionary of alerts to list of users that have seen it."""
        return {alert: self.get_seen_by(alert) for alert in self.alerts}

    def flush(self) -> None:
        """Delete all alerts from database."""
        self._exec_sql("DELETE FROM alerts")

    def flush_user(self, user: str) -> None:
        """Delete all alerts for a specific user from database."""
        self._exec_sql("DELETE FROM alerts WHERE user = (?)", (user,))
