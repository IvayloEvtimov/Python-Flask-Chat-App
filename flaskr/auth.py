import functools
import os
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
UPLOAD_AVATAR_FOLDER = "static/chats/avatar/"


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif (
            db.execute(
                "SELECT username FROM user WHERE username = ?", (username,)
            ).fetchone()
            is not None
        ):
            error = f"User {username} is already registered."

        if error is None:
            db.execute(
                "INSERT INTO user (username, avatar, password) VALUES (?, ?, ?)",
                (username, "default.png", generate_password_hash(password)),
            )
            db.commit()
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if (user is None) or (not check_password_hash(user["password"], password)):
            error = "Incorrect username or password"

        if error is None:
            session.clear()
            session["username"] = user["username"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    user = session.get("username")

    if user is None:
        g.user = None
    else:
        g.user = (
            get_db()
            .execute("SELECT * FROM user WHERE username = ?", (user,))
            .fetchone()
        )


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
@bp.route("/changePassword", methods=("GET", "POST"))
def changePassword():
    if request.method == "POST":
        db = get_db()

        username = g.user["username"]
        new_password = request.form["password"]

        db.execute(
            "UPDATE user SET password = ? WHERE username = ?",
            (generate_password_hash(new_password), username),
        )
        db.commit()

        return redirect(url_for("index"))

    return render_template("auth/changePassword.html")

        return view(**kwargs)

    return wrapped_view