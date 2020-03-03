"""Config command"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import yaml
import logging

gef_config_dir = os.path.expanduser('~') + '/.gef.yml'

def set(var_name, value):
    with open(gef_config_dir, 'r+') as infile:
        data = yaml.load(infile, Loader=yaml.FullLoader)
        with open(gef_config_dir, 'w+') as outfile:
            if data is None:
                data = {}
            data[var_name] = value
            yaml.dump(data, outfile, default_flow_style=False)
    return True

def show(var_name, value):
    with open(gef_config_dir, 'r+') as outfile:
        data = yaml.load(outfile, Loader=yaml.FullLoader)
        if data is not None:
            print('Value: ' + str(data[var_name]))
    return True

def get(var_name):
    with open(gef_config_dir, 'r+') as outfile:
        data = yaml.load(outfile, Loader=yaml.FullLoader)
        if data is not None and var_name in data:
            return data[var_name]
        return ''
    return True

def unset(var_name, value):
    with open(gef_config_dir, 'r+') as infile:
        data = yaml.load(infile, Loader=yaml.FullLoader)
        with open(gef_config_dir, 'w+') as outfile:
            if data is not None:
                data.pop(var_name, None)
                yaml.dump(data, outfile, default_flow_style=False)
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
