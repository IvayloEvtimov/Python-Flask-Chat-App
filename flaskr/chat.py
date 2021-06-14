from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

import json

bp = Blueprint("chat", __name__)


@bp.route("/")
def index():
    db = get_db()

    return render_template("chat/index.html")


@bp.route("/search", methods=["POST"])
def searchContact():
    db = get_db()

    username = request.form["username"]

    users = db.execute(
        "SELECT username FROM user WHERE username LIKE ?", (username,)
    ).fetchall()

    if len(users) == 0:
        return json.dumps([])


