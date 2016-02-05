import flask

from libs import api


def do():
    return flask.render_template("/tools/create_agent_link/new.html", clients=api.remote_management.client.get_all())