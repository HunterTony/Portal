import flask
import os


def do(document):
    if(document is None):
        document = "introduction"

    if(not os.path.exists("templates/documentation/{}.html".format(document))):
        flask.abort(404)

    return flask.render_template("/documentation/{}.html".format(document))