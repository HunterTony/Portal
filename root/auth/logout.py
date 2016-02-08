import flask

from libs import render


def do():
    flask.session.clear()

    return render.success("Auth Success", "Logout successful.")