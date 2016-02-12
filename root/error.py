import flask
import os
import traceback
import sys
import hashlib

from libs import log


def init(app):
    @app.errorhandler(400) # Bad request
    def error_handler_400(e):
        return flask.render_template("/error/400.html"), 400


    @app.errorhandler(404) # File not found
    def error_handler_404(e):
        return flask.render_template("/error/404.html"), 404


    @app.errorhandler(500) # Internal server error
    def error_handler_500(e):
        exception = {}

        hash = hashlib.sha256()
        hash.update(os.urandom(8))
        exception["id"] = hash.hexdigest()

        exception["value"], exception["type"], exception["traceback"] = sys.exc_info()
        exception["traceback"] = traceback.extract_tb(exception["traceback"])

        log.error("An unhandled exception occurred:")
        log.error("ID:        " + exception["id"])
        log.error("Type:      " + repr(exception["type"]))
        log.error("Value:     " + repr(exception["value"]))
        log.error("Traceback: ")

        for Frame in exception["traceback"]:
            log.error(str(Frame))

        return flask.render_template("/error/500.html", exception=exception), 500
