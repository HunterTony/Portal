import flask

from . import tools


def init(app):
    @app.route("/")
    def root():
        return flask.render_template("/root.html")

    tools.route.init(app)