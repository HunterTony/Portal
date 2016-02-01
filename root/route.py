import flask


def init(app):
    @app.route("/")
    def root():
        return flask.render_template("/root.html")
