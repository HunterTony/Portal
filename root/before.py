import flask

from libs import log


def init(app):
    @app.before_request
    def before_request():
        ### Request Logging ###
        details = [
            {"parameters":      dict(flask.request.args)},
            {"data":            dict(flask.request.form)},
            {"remote_addr":     flask.request.remote_addr},
            {"x_forwarded_for": flask.request.headers.get("X-Forwarded-For")},
            {"user":            flask.session["user_id"] if "user_id" in flask.session else None},
        ]

        log.info("{0} {1}>".format(str(flask.request).rstrip(">"), details))
