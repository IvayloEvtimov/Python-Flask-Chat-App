import pytest

from flaskr import create_app


def test_config():
    """Test create_app without passing test config."""
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing


def test_index(client):
    response = client.get("/")
    assert (
        response.data
        == b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>Redirecting...</title>\n<h1>Redirecting...</h1>\n<p>You should be redirected automatically to target URL: <a href="/auth/login">/auth/login</a>.  If not click the link.'
    )


def test_index_redirect(client):
    response = client.get("/")
    redirect = client.get(response.location)
    assert redirect.status_code == 200