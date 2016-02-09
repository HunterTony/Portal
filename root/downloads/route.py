from . import view


def init(app):
    @app.route("/downloads")
    def download_view():
        return view.do()