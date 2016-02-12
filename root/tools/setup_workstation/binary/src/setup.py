import sys
sys.dont_write_bytecode = True

import requests
import json


def load_config():
    with open("C:\\Cilix\\config.json", "r") as fp:
        config = json.loads(fp.read())

    return config


def download_action(action):
    print("  Downloading '{}'".format(action))

    return requests.get("https://portal.cilix.co.uk/tools/setup_workstation/action_download/{}".format(action)).content.decode()


def execute_action(action, action_data):
    print("  Executing '{}'".format(action))

    exec(action_data)


def run_setup(config):
    for action in config["actions"]:
        action_data = download_action(action)
        execute_action(action, action_data)


def main():
    config = load_config()

    run_setup(config)


if(__name__ == "__main__"):
    main()
