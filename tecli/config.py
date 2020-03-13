"""Config command"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import yaml
import logging

config_path = os.path.expanduser('~') + '/.tecli.yml'

# Default values that can be altered in local .tecli.yml file
config = {
    'url_api': 'https://api.trends.earth'
}

def set(var_name, value):
    with open(config_path, 'r+') as infile:
        config.update(yaml.load(infile, Loader=yaml.FullLoader))
        with open(config_path, 'w+') as outfile:
            if config is None:
                config = {}
            config[var_name] = value
            yaml.dump(config, outfile, default_flow_style=False)
    return True

def show(var_name, value):
    with open(config_path, 'r+') as infile:
        config.update(yaml.load(infile, Loader=yaml.FullLoader))
        if config is not None:
            print('Value: ' + str(config[var_name]))
    return True

def get(var_name):
    with open(config_path, 'r+') as infile:
        config.update(yaml.load(infile, Loader=yaml.FullLoader))
        if config is not None and var_name in config:
            return config[var_name]
        return ''
    return True

def unset(var_name, value):
    with open(config_path, 'r+') as infile:
        config.update(yaml.load(infile, Loader=yaml.FullLoader))
        with open(config_path, 'w+') as outfile:
            if config is not None:
                config.pop(var_name, None)
                yaml.dump(config, outfile, default_flow_style=False)
    return True

ACTIONS = {
    "set": set,
    "show": show,
    "unset": unset
}

def run(action, var_name, value):
    """Config command"""
    action_method = ACTIONS[action]
    if action_method:
        return action_method(var_name, value)
    else:
        logging.error('Action not found')
        return False
