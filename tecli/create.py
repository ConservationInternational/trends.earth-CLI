"""Create command"""

import json
import logging
import os
from shutil import copytree


def is_valid(name):
    """Check if the name is valid"""
    return bool(name)


def create_config_file(name):
    """Create a JSON configuration file"""
    config = {}
    config["name"] = name
    to_dir = os.getcwd() + "/" + name
    with open(os.path.join(to_dir, "configuration.json"), "w") as config_file:
        json.dump(config, config_file)


def run():
    """Create command"""
    name = None
    while name is None or not is_valid(name):
        name = input("Please enter the project name: ")

    try:
        to_dir = os.getcwd() + "/" + name
        from_dir = os.path.dirname(os.path.realpath(__file__)) + "/skeleton"

        copytree(from_dir, to_dir)
        create_config_file(name)
    except Exception as error:
        logging.error(error)
        return False

    return True
