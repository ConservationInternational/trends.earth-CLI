"""Config command"""

import logging
import os

import yaml

config_path = os.path.expanduser("~") + "/.tecli.yml"

# Default values that can be altered in local .tecli.yml file
settings = {"url_api": "https://api.trends.earth"}


def set(var_name, value):
    global settings
    if os.path.exists(config_path):
        with open(config_path, "r") as infile:
            file_settings = yaml.load(infile, Loader=yaml.FullLoader)
            if file_settings:
                settings.update(file_settings)
    settings[var_name] = value
    with open(config_path, "w") as outfile:
        yaml.dump(settings, outfile, default_flow_style=False)
    return True


def show(var_name, value):
    global settings
    if os.path.exists(config_path):
        with open(config_path, "r") as infile:
            file_settings = yaml.load(infile, Loader=yaml.FullLoader)
            if file_settings:
                settings.update(file_settings)
    if settings is not None:
        print("Value: " + str(settings.get(var_name, "")))
    return True


def get(var_name):
    global settings
    if not os.path.exists(config_path):
        return settings.get(var_name, "")
    with open(config_path, "r") as infile:
        file_settings = yaml.load(infile, Loader=yaml.FullLoader)
        if file_settings:
            settings.update(file_settings)
    return settings.get(var_name, "")


def unset(var_name, value):
    global settings
    if os.path.exists(config_path):
        with open(config_path, "r") as infile:
            file_settings = yaml.load(infile, Loader=yaml.FullLoader)
            if file_settings:
                settings.update(file_settings)
    settings.pop(var_name, None)
    with open(config_path, "w") as outfile:
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
