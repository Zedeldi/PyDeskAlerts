"""Web interface for the DeskAlerts network."""

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
        db.add_message(user, message)
        status = "Success!"
    return render_template("send.html", status=status)


@app.route("/get", methods=["GET"])
def get() -> str:
    """Endpoint to get messages from server."""
    user = request.args.get("user")
    d = {
        "messages": db.get_messages(user),
    }
    return d
