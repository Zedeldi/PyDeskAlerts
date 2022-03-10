"""Web interface for the DeskAlerts network."""

from datetime import datetime

from flask import Flask, render_template, request

from deskalerts.server.db import DB

app = Flask(__name__)
db = DB()


@app.route("/send", methods=["POST", "GET"])
def send() -> str:
    """Endpoint to send input to server."""
    status = None
    if request.method == "POST":
        user = request.form["user"]
        message = request.form["message"]
        expires = datetime.strptime(request.form["expires"], "%Y-%m-%d").timestamp()
        db.add_message(user, message, expires)
        status = "Success!"
    return render_template("send.html", all_users=db.ALL_USERS, status=status)


@app.route("/get", methods=["GET"])
def get() -> dict[str, list[str]]:
    """Endpoint to get messages from server."""
    user = request.args.get("user")
    d = {
        "messages": db.get_messages(user),
    }
    return d
