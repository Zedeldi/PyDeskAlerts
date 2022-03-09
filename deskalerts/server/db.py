"""Database interface and operations."""

import sqlite3
import time
from typing import Any


class DB:
    """Handle database operations."""

    def __init__(self, database: str = "deskalerts.db") -> None:
        """Initialise database."""
        self.database = database
        self._exec_sql(
            "CREATE TABLE IF NOT EXISTS alerts (user STRING, message STRING, time REAL)"
        )

    def _exec_sql(self, *args) -> list[Any]:
        """Execute SQL in database and return results."""
        conn = sqlite3.connect(self.database)
        cur = conn.cursor()
        with conn:
            res = cur.execute(*args).fetchall()
        conn.close()
        return res

    def add_message(self, user: str, message: str) -> None:
        """Add message to database."""
        self._exec_sql(
            "INSERT INTO alerts VALUES (?, ?, ?)", (user, message, time.time())
        )

    def get_messages(self, user: str) -> list[str]:
        """
        Return all messages for user in database.

        All messages for the user are deleted afterwards.
        """
        messages = [
            message[0]
            for message in self._exec_sql(
                "SELECT message FROM alerts WHERE user = (?)", (user,)
            )
        ]
        self.flush_user(user)
        return messages

    def flush(self) -> None:
        """Delete all alerts from database."""
        self._exec_sql("DELETE FROM alerts")

    def flush_user(self, user: str) -> None:
        """Delete all alerts for a specific user from database."""
        self._exec_sql("DELETE FROM alerts WHERE user = (?)", (user,))
