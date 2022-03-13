from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from flask.globals import session
from flask.helpers import send_from_directory
from flask.sessions import NullSession
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

# from flaskr.auth import login_required
from flaskr.db import get_db

from . import auth

import time

import random
import string
import json
import os

UPLOAD_IMG_FOLDER = "static/chats/img/"
UPLOAD_VID_FOLDER = "static/chats/vid/"
UPLOAD_AVATAR_FOLDER = "static/chats/avatar/"
ALLOWED_IMG_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
ALLOWED_VID_EXTENSIONS = {"mp4", "webm", "oog"}

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))


bp = Blueprint("chat", __name__)


@bp.route("/")
def index():
    # db = get_db()

    if session.get("username") == None:
        return redirect("/auth/login")

    return render_template("chat/index.html")


@bp.route("/syncChat", methods=["POST"])
def syncChat():
    db = get_db()

    recipient1 = request.form["recipient"]
    recipient2 = session["username"]

    loaded_messages = int(request.form["loaded_messages"])

    chat_file_path = db.execute(
        "SELECT chat_file FROM person_chat WHERE (recipient1 = ? AND recipient2 = ?) OR (recipient2 = ? AND recipient1 = ?)",
        (recipient1, recipient2, recipient1, recipient2),
    ).fetchone()

    data = json.load(open(os.path.join(SITE_ROOT, "static/chats", chat_file_path[0])))

    # return json.dumps(data)
    output = []

    if len(data) > loaded_messages:
        for count in range(loaded_messages, len(data)):
            # output.update(data[count])
            output.append(data[count])

        return json.dumps(output)

    return json.dumps([])


@bp.route("/loadContacts", methods=["POST"])
def loadContacts():
    db = get_db()

    username = session["username"]

    contacts = db.execute(
        "SELECT recipient1,recipient2 FROM person_chat WHERE recipient1 = ? OR recipient2 = ?",
        (username, username),
    ).fetchall()

    if len(contacts) == 0:
        return json.dumps([])

    output = []

    for user in contacts:
        if user[0] != username:
            output.append(user[0])
        else:
            output.append(user[1])

    return json.dumps(output)


@bp.route("/search", methods=["POST"])
def searchContact():
    db = get_db()

    username = request.form["username"]

    users = db.execute(
        "SELECT username FROM user WHERE username LIKE ?", (username,)
    ).fetchall()

    if len(users) == 0:
        return json.dumps([])

    return json.dumps([dict(user) for user in users])


@bp.route("/loadChat", methods=["POST"])
def loadChat():
    db = get_db()

    recipient1 = request.form["recipient"]
    recipient2 = session["username"]

    chat_file_path = db.execute(
        "SELECT chat_file FROM person_chat WHERE (recipient1 = ? AND recipient2 = ?) OR (recipient2 = ? AND recipient1 = ?)",
        (recipient1, recipient2, recipient1, recipient2),
    ).fetchone()

    if chat_file_path is None:
        chat_file_path = string.ascii_letters
        chat_file_path = "".join(random.choice(chat_file_path) for i in range(10))

        # SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(SITE_ROOT, "static/chats", chat_file_path)

        with open(json_url, "w") as file:
            file.write("[]")
            file.close()

        db.execute(
            "INSERT INTO person_chat (recipient1,recipient2,chat_file) VALUES  (?,?,?)",
            (recipient1, recipient2, chat_file_path),
        )
        db.commit()
        return json.dumps([])

    # SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    # json_url = os.path.join(SITE_ROOT, "static/chats", chat_file_path[0])
    data = json.load(open(os.path.join(SITE_ROOT, "static/chats", chat_file_path[0])))

    return json.dumps(data)


@bp.route("/sendMessage", methods=["POST"])
def sendMessage():
    db = get_db()

    receiver = request.form["recipient"]
    sender = session["username"]

    message = request.form["message"]
    seconds = int(time.time())

    chat_file_path = db.execute(
        "SELECT chat_file FROM person_chat WHERE (recipient1 = ? AND recipient2 = ?) OR (recipient2 = ? AND recipient1 = ?)",
        (receiver, sender, receiver, sender),
    ).fetchone()

    # SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/chats", chat_file_path[0])

    dict = {"sender": sender, "time": seconds, "message": message}

    with open(json_url, "r+") as file:
        data = json.load(file)
        data.append(dict)
        file.seek(0)
        json.dump(data, file)
        file.close()

    return json.dumps(dict)


def allowed_img_file(filename):
    return (
        "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMG_EXTENSIONS
    )


@bp.route("/uploads/<name>")
def loadImage(name):
    return send_from_directory(UPLOAD_IMG_FOLDER, name)


@bp.route("/sendImage", methods=["POST"])
def sendImage():
    db = get_db()

    receiver = request.form["recipient"]
    sender = session["username"]

    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)

    file = request.files["file"]

    if file.filename == "":
        flash("No selected file")
        return redirect(request.url)

    if not file and not allowed_img_file(file.filename):
        flash("No selected file")
        return redirect(request.url)

    filename = secure_filename(file.filename)
    file.save(os.path.join(SITE_ROOT, UPLOAD_IMG_FOLDER, filename))

    chat_file_path = db.execute(
        "SELECT chat_file FROM person_chat WHERE (recipient1 = ? AND recipient2 = ?) OR (recipient2 = ? AND recipient1 = ?)",
        (receiver, sender, receiver, sender),
    ).fetchone()

    dict = {
        "sender": sender,
        "time": int(time.time()),
        "type": "img",
        "url": url_for("loadImage", name=filename),
    }

    with open(os.path.join(SITE_ROOT, "static/chats", chat_file_path[0]), "r+") as file:
        data = json.load(file)
        data.append(dict)
        file.seek(0)
        json.dump(data, file)
        file.close()

    return json.dumps(dict)


def allowed_vid_file(filename):
    return (
        "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_VID_EXTENSIONS
    )


@bp.route("/loadVid/<name>")
def loadVid(name):
    return send_from_directory(UPLOAD_VID_FOLDER, name)


@bp.route("/sendVideo", methods=["POST"])
def sendVideo():
    db = get_db()

    receiver = request.form["recipient"]
    sender = session["username"]

    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)

    file = request.files["file"]

    if file.filename == "":
        flash("No selected file")
        return redirect(request.url)

    if not file and not allowed_vid_file(file.filename):
        flash("No selected file")
        return redirect(request.url)

    filename = secure_filename(file.filename)
    file.save(os.path.join(SITE_ROOT, UPLOAD_VID_FOLDER, filename))

    chat_file_path = db.execute(
        "SELECT chat_file FROM person_chat WHERE (recipient1 = ? AND recipient2 = ?) OR (recipient2 = ? AND recipient1 = ?)",
        (receiver, sender, receiver, sender),
    ).fetchone()

    dict = {
        "sender": sender,
        "time": int(time.time()),
        "type": "vid",
        "url": url_for("loadVid", name=filename),
    }

    with open(os.path.join(SITE_ROOT, "static/chats", chat_file_path[0]), "r+") as file:
        data = json.load(file)
        data.append(dict)
        file.seek(0)
        json.dump(data, file)
        file.close()

    return json.dumps(dict)