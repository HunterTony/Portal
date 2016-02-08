import flask

from . import auth
from . import tools


def init(app):
    @app.route("/")
    def root():
        return flask.render_template("/root.html")

    auth.route.init(app)
    tools.route.init(app)