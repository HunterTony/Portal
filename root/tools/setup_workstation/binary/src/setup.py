import sys
sys.dont_write_bytecode = True

import requests
import json
import imp


def load_config():
    with open("C:\\Cilix\\config.json", "r") as fp:
        config = json.loads(fp.read())

    return config


def execute_package(package):
    print("  Executing '{}'".format(package["name"]))

    module = imp.new_module(package["name"])
    exec(package["script"], module.__dict__)


def run_setup(config):
    for package in config["packages"]:
        execute_package(package)


def main():
    config = load_config()

    run_setup(config)


if(__name__ == "__main__"):
    main()
