import flask


def do():
    return flask.render_template("/auth/redirect.html")