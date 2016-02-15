import flask
import os
import json
import subprocess
import uuid
import io

import config
from libs import api
from libs import render
from libs import exception
from libs import package

from root.tools.create_agent_link.post import create_agent

from . import new


def compile_setup_binary(config):
    with open("root/tools/setup_workstation/binary/config.json", "w") as fp:
        fp.write(json.dumps(config))

    file_name = "/tmp/{}.exe".format(str(uuid.uuid4()))

    with subprocess.Popen(["make", "-C" "root/tools/setup_workstation/binary", "TARGET_FILENAME=" + file_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        stdout = process.stdout.read().decode()
        stderr = process.stderr.read().decode()

    os.remove("root/tools/setup_workstation/binary/config.json")

    if(len(stderr) > 1):
        raise exception.SetupWorkstationError(stderr)

    with open(file_name, "rb") as fp:
        setup_binary = fp.read()

    os.remove(file_name)

    return setup_binary


def do():
    client = api.remote_management.client.get_from_id(int(flask.request.form["client"]))
    site   = api.remote_management.site.get_from_id(client["id"], int(flask.request.form["site"]))
    agent_hash = create_agent(client, site)

    selected_packages = []
    for pack in package.get_for_application("setup"):
        if(flask.request.form.get(pack["name"]) is not None):
            selected_packages.append(pack)

    config = {
        "agent_hash": agent_hash,
        "packages":   selected_packages,
    }

    try:
        setup_binary = compile_setup_binary(config)
    except exception.SetupWorkstationError as error:
        return render.error("Setup Workstation Error", "Failed to compile setup binary: '{0}'".format(error), "/tools/setup_workstation")

    setup_binary_file = io.BytesIO(setup_binary)

    return flask.send_file(setup_binary_file, mimetype="application/x-msdownload", as_attachment=True, attachment_filename="Setup_Workstation.exe")
