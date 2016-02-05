import flask
import hashlib
import os


def init(app):
    @app.context_processor
    def _csrf_token_():
        if("_CSRF_TOKEN_" not in flask.session):
            Hash = hashlib.sha256()
            Hash.update(os.urandom(128))
            flask.session["_CSRF_TOKEN_"] = Hash.hexdigest()

        return {
            "_CSRF_TOKEN_": flask.session["_CSRF_TOKEN_"],
        }


    @app.before_request
    def check_token():
        if(flask.request.method == "POST" or flask.request.form):
            if("_CSRF_TOKEN_" not in flask.session):
                flask.abort(400)

            if(flask.request.form["_CSRF_TOKEN_"] != flask.session["_CSRF_TOKEN_"]):
                flask.abort(400)
