"""Web interface for the DeskAlerts network."""

import time
from datetime import datetime
from typing import Any

from flask import Flask, render_template, request

from deskalerts.server.db import DB, Alert

app = Flask(__name__)
db = DB()


@app.route("/send", methods=["POST", "GET"])
def send() -> str:
    """Endpoint to send input to server."""
    status = None
    if request.method == "POST":
        alert = Alert(
            user=request.form["user"],
            message=request.form["message"],
            created=time.time(),
            expires=datetime.strptime(request.form["expires"], "%Y-%m-%d").timestamp(),
        )
        db.add_alert(alert)
        status = "Success!"
    return render_template("send.html", all_users=db.ALL_USERS, status=status)


@app.route("/get", methods=["GET"])
def get() -> dict[str, Any]:
    """Endpoint to get alerts from server."""
    user = request.args.get("user")
    d = {
        "alerts": db.get_alerts(user),
    }
    return d


@app.route("/stats", methods=["GET"])
def stats() -> dict[str, Any]:
    """Endpoint to get statistics about the database."""
    return {
        "alerts": db.alerts,
        "users": db.seen_users,
    }
