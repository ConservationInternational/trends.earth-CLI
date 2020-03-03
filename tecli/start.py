"""Create command"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tempfile
import os
import json
import subprocess
import time
import logging
import base64

from tecli import config
from shutil import copytree, copyfile


def query_to_dict(query):
    params = query.split('&')
    query_data = {}
    for param in params:
        key, value = param.split('=')
        query_data[key] = value
    return query_data

def read_gee_service_account():
    """Obtain jwt token of config user"""
    return config.get('EE_SERVICE_ACCOUNT_JSON')

def build_docker(tempdir, dockerid):
    """Build docker"""
    try:
        subprocess.run("docker build -t {0} .".format(dockerid), shell=True, check=True, cwd=tempdir)
        return True
    except subprocess.CalledProcessError as error:
        logging.error(error)
        return False


def run_docker(tempdir, dockerid, param):
    """Run docker"""
    try:
        service_account = read_gee_service_account()
        subprocess.run("docker run -e ENV=dev -e EE_SERVICE_ACCOUNT_JSON={2} --rm {0} {1}".format(dockerid, param, service_account), shell=True, check=True, cwd=tempdir)
        return True
    except subprocess.CalledProcessError as error:
        logging.error(error)
        return False


def run(param, payload):
    """Start command"""
    logging.debug('Creating temporary file...')
    # Current folder
    cwd = os.getcwd()
    # Getting Dockerfile from /run folder
    dockerfile = os.path.dirname(os.path.realpath(__file__)) + '/run/Dockerfile'

    payload_data = {}
    if payload and payload != '':
        try:
            with open(payload) as data_file:
                payload_data = dict(json.load(data_file))
        except Exception as error:
            logging.error(error)
            return False

    with tempfile.TemporaryDirectory() as tmpdirname:
        logging.debug('Copying Dockerfile ...')
        copyfile(dockerfile, tmpdirname + '/Dockerfile')

        logging.debug('Copying src folder ...')
        copytree(cwd + '/src', tmpdirname + '/src')

        logging.debug('Copying requirements ...')
        copyfile(cwd + '/requirements.txt', tmpdirname + '/requirements.txt')

        logging.debug('Building ...')
        dockerid = 'gef-local-'+str(time.time())
        success = False
        if build_docker(tmpdirname, dockerid):
            logging.debug('Running script ....')
            logging.info(param)
            param_dict = query_to_dict(param) if param != '' else {}
            param_dict.update(payload_data)
            param_serial = json.dumps(param_dict).encode('utf-8')
            param_serial = base64.b64encode(param_serial)
            success = run_docker(tmpdirname, dockerid, param_serial)

        return success
