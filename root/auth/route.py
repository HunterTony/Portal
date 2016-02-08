from . import redirect
from . import login
from . import logout


def init(app):
    @app.route("/auth/redirect")
    def auth_redirect():
        return redirect.do()

    @app.route("/auth/login", methods=["POST"])
    def auth_login():
        return login.do()

    @app.route("/auth/logout", methods=["POST"])
    def auth_logout():
        return logout.do()