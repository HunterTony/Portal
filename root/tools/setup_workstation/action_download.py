import flask


def do(action_name):
    if("." in action_name or action_name[0] == "/"):
        flask.abort(404)

    action_filename = (action_name + ".py").lower()

    return flask.send_from_directory("root/tools/setup_workstation/actions", action_filename)
