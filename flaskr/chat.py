from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("chat", __name__)


@bp.route("/")
def index():
    db = get_db()

    return render_template("chat/index.html")
