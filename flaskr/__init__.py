import os

from flask import Flask
from . import chat
from . import auth
from . import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    app.register_blueprint(auth.bp)

    app.register_blueprint(chat.bp)
    app.add_url_rule("/", endpoint="index")
    app.add_url_rule("/syncChat", endpoint="syncChat")
    app.add_url_rule("/avatar/<name>", endpoint="loadAvatar", build_only=True)
    app.add_url_rule("/loadContacts", endpoint="loadContacts")
    app.add_url_rule("/search", endpoint="searchContact")
    app.add_url_rule("/loadChat", endpoint="loadChat")
    app.add_url_rule("/sendMessage", endpoint="sendMessage")
    app.add_url_rule("/sendImage", endpoint="sendImage")
    app.add_url_rule("/uploads/<name>", endpoint="loadImage", build_only=True)
    app.add_url_rule("/sendVideo", endpoint="sendVideo")
    app.add_url_rule("/loadVid/<name>", endpoint="loadVid", build_only=True)
    app.add_url_rule("/sendLocation", endpoint="sendLocation")

    return app
