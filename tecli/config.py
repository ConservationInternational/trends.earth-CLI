"""Config command"""

import logging
import os

import yaml

config_path = os.path.expanduser("~") + "/.tecli.yml"

# Default values that can be altered in local .tecli.yml file
settings = {"url_api": "https://api.trends.earth"}


def set(var_name, value):
    global settings
    with open(config_path, "r+") as infile:
        settings.update(yaml.load(infile, Loader=yaml.FullLoader))
        with open(config_path, "w+") as outfile:
            if settings is None:
                settings = {}
            settings[var_name] = value
            yaml.dump(settings, outfile, default_flow_style=False)
    return True


def show(var_name, value):
    global settings
    with open(config_path, "r+") as infile:
        settings.update(yaml.load(infile, Loader=yaml.FullLoader))
        if settings is not None:
            print("Value: " + str(settings[var_name]))
    return True


def get(var_name):
    global settings
    with open(config_path, "r+") as infile:
        settings.update(yaml.load(infile, Loader=yaml.FullLoader))
        if settings is not None and var_name in settings:
            return settings[var_name]
        return ""
    return True


def unset(var_name, value):
    global settings
    with open(config_path, "r+") as infile:
        settings.update(yaml.load(infile, Loader=yaml.FullLoader))
        with open(config_path, "w+") as outfile:
            if settings is not None:
                settings.pop(var_name, None)
                yaml.dump(settings, outfile, default_flow_style=False)
    return True


ACTIONS = {"set": set, "show": show, "unset": unset}


def run(action, var_name, value):
    """Config command"""
    action_method = ACTIONS[action]
    if action_method:
        return action_method(var_name, value)
    else:
        logging.error("Action not found")
        return False
