import flask
import os

from libs import api


def get_actions():
    action_files = os.listdir("root/tools/setup_workstation/actions/")
    actions = [action.rstrip(".py") for action in action_files if action[0] != "."]
    actions = sorted(actions)

    return actions


def do():
    actions = get_actions()

    return flask.render_template("/tools/setup_workstation/new.html", clients=api.remote_management.client.get_all(), actions=actions)
