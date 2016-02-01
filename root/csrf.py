import flask
import hashlib
import os


def init(app):
    @app.template_global("get_csrf_token")
    def get_csrf_token():
        if("_CSRF_TOKEN_" not in flask.session):
            Hash = hashlib.sha256()
            Hash.update(os.urandom(128))
            flask.session["_CSRF_TOKEN_"] = Hash.hexdigest()

        return flask.session["_CSRF_TOKEN_"]


    @app.before_request
    def check_token():
        if(flask.request.method == "POST" or flask.request.form):
            if("_CSRF_TOKEN_" not in flask.session):
                flask.abort(400)

            if(flask.request.form["_CSRF_TOKEN_"] != flask.session["_CSRF_TOKEN_"]):
                flask.abort(400)
