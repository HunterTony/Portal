import flask

from libs import log
from . import auth


auth_excluded_endpoints = ["auth_redirect", "auth_login", "static"]


def init(app):
    @app.before_request
    def before_request():
        ### Request Logging ###
        details = {
            "parameters":      dict(flask.request.args),
            "data":            dict(flask.request.form),
            "remote_addr":     flask.request.remote_addr,
            "x_forwarded_for": flask.request.headers.get("X-Forwarded-For"),
            "username":        flask.session["username"] if "username" in flask.session else None,
        }

        if("username" in details["data"]):
            details["data"]["username"] = "... REDACTED ..."
        if("password" in details["data"]):
            details["data"]["password"] = "... REDACTED ..."

        log.info("{0} {1}>".format(str(flask.request).rstrip(">"), details))

        ### Check CSRF Token ###
        if(flask.request.method == "POST" or flask.request.form):
            if("_CSRF_TOKEN_" not in flask.session):
                flask.abort(400)

            if(flask.request.form["_CSRF_TOKEN_"] != flask.session["_CSRF_TOKEN_"]):
                flask.abort(400)

        ### Check Auth State ###
        if(flask.request.endpoint in auth_excluded_endpoints):
            return None

        if(not auth.check.client_authed()):
            flask.session["auth_return_url"] = flask.request.path
            return flask.redirect(flask.url_for("auth_redirect"), 302)

