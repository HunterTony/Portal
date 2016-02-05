import flask

from libs import data


def do():
    return flask.render_template("/tools/password_generator/new.html", available_dictionaries=data.dictionary.available)