import sqlite3
import pytest

from sqlite3 import Row

from flask.globals import session
from flaskr.db import get_db


@pytest.mark.parametrize(
    ("username", "result"),
    (
        ("test_user", Row),
        ("test_fake_user", type(None)),
    ),
)
def test_register(client, app, username, result):
    assert client.get("/auth/register").status_code == 200

    response = client.post(
        "/auth/register", data={"username": "test_user", "password": "test_user"}
    )
    assert response.location == "http://localhost/auth/login"

    with app.app_context():
        assert (
            isinstance(
                get_db()
                .execute("SELECT * FROM user WHERE username=?", (username,))
                .fetchone(),
                result,
            )
            is True
        )


def test_login(client, auth):
    assert client.get("/auth/login").status_code == 200

    response = auth.login()
    assert response.location == "http://localhost/"

    with client:
        client.get("/")
        assert session["username"] != None


@pytest.mark.parametrize(
    ("username", "result"),
    (
        ("test", True),
        ("Fake_user", False),
    ),
)
def test_login_specific_username(client, auth, username, result):
    assert client.get("/auth/login").status_code == 200

    response = auth.login()
    assert response.location == "http://localhost/"

    with client:
        client.get("/")
        assert (session["username"] == username) is result


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("", "", b"Username is required."),
        ("test", "", b"Password is required."),
        ("test", "test", b"User test is already registered"),
    ),
)
def test_register_validate_input(client, username, password, message):
    response = client.post(
        "/auth/register",
        data={"username": username, "password": password},
    )
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert "username" not in session


def test_change_pass_get(client):
    response = client.get("/auth/changePassword")
    assert response.status_code == 200


def test_login_error(client):
    response_register = client.post(
        "/auth/register", data={"username": "test_user", "password": "test_user"}
    )
    # assert response_register.status_code == 200

    response = client.post("/auth/login", data={"username": "test", "password": "pass"})
    assert b"Incorrect username or password" in response.data


@pytest.mark.parametrize(
    ("password", "result"),
    (
        ("test123", False),
        ("diff_pass", True),
    ),
)
def test_change_pass_post(client, auth, password, result):
    auth.login()
    with client:
        client.get("/")
        assert "username" in session

    auth.changePassword("test123")

    auth.logout()
    with client:
        client.get("/")
        assert "username" not in session

    response = auth.login("test", password)
    assert (b"Incorrect username or password" in response.data) == result
