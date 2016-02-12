import flask
import os

import config
from libs import api


def create_agent(client, site):
    agent      = api.remote_management.agent.get(client, site)
    agent_hash = api.remote_management.agent.get_hash(client, site)

    try:
        os.mkdir(config.remote_management.local_agent_path + agent_hash)
    except FileExistsError:
        pass

    with open(config.remote_management.local_agent_path + agent_hash + "/agent.exe", "wb") as fp:
        fp.write(agent)

    return agent_hash


def do():
    client = api.remote_management.client.get_from_id(int(flask.request.form["client"]))
    site   = api.remote_management.site.get_from_id(client["id"], int(flask.request.form["site"]))
    agent_hash = create_agent(client, site)

    return flask.render_template("/tools/create_agent_link/view.html", client=client, site=site, agent_hash=agent_hash)
