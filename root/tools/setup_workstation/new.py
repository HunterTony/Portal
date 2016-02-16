import flask
import os

from libs import api
from libs import package


def do():
    return flask.render_template("/tools/setup_workstation/new.html", clients=api.remote_management.client.get_all(), packages=package.get_all())
