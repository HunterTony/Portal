from . import view


def init(app):
    @app.route("/documentation")
    @app.route("/documentation/<path:document>")
    def documentation_view(document=None):
        return view.do(document)