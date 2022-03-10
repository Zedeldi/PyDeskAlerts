"""Database interface and operations."""

import sqlite3
import time
from typing import Any


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

    def add_message(self, user: str, message: str, expires: float) -> None:
        """Add message to database."""
        self._exec_sql(
            "INSERT INTO alerts VALUES (null, ?, ?, ?, ?)",
            (user, message, time.time(), expires),
        )

    def _get_messages(self, user: str) -> list[tuple[int, str]]:
        """
        Return all valid messages for the specified user and self.ALL_USERS.

        Add message ID and user to seen table.
        """
        messages = [
            (message[0], message[1])
            for message in self._exec_sql(
                """
                SELECT id, message
                FROM alerts
                WHERE (user = (?) OR user = (?))
                AND expires > (?)
                AND id NOT IN
                (SELECT id FROM seen WHERE user = (?))
                """,
                (user, self.ALL_USERS, time.time(), user),
            )
        ]
        for message_id, _ in messages:
            self._exec_sql("INSERT INTO seen VALUES (?, ?)", (message_id, user))
        return messages

    def get_messages(self, user: str) -> list[str]:
        """Return all unseen, unexpired messages for user in database."""
        return [message[1] for message in self._get_messages(user)]

    def flush(self) -> None:
        """Delete all alerts from database."""
        self._exec_sql("DELETE FROM alerts")

    def flush_user(self, user: str) -> None:
        """Delete all alerts for a specific user from database."""
        self._exec_sql("DELETE FROM alerts WHERE user = (?)", (user,))
