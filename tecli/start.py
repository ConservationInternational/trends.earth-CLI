"""Create command"""

import base64
import json
import logging
import os
import subprocess
import tempfile
import time
from shutil import copyfile, copytree

from tecli import config

from .info import read_configuration


def query_to_dict(query):
    params = query.split("&")
    query_data = {}
    for param in params:
        key, value = param.split("=")
        query_data[key] = value
    return query_data


def read_gee_service_account():
    """Obtain jwt token of config user"""
    return config.get("EE_SERVICE_ACCOUNT_JSON")


def build_docker(tempdir, dockerid):
    """Build docker"""
    try:
        config = read_configuration()
        environment = config.get("environment", "trends.earth-environment")
        environment_version = config.get("environment_version", "0.1.6")
        logging.debug(f"Building with environment {environment}:{environment_version}...")
        subprocess.run(
            f'docker build --build-arg="ENVIRONMENT={environment}" --build-arg="ENVIRONMENT_VERSION={environment_version}" -t {dockerid} .',
            shell=True,
            check=True,
            cwd=tempdir,
        )
        return True
    except subprocess.CalledProcessError as error:
        logging.error(error)
        return False


def run_docker(tempdir, dockerid, param):
    """Run docker"""
    try:
        service_account = read_gee_service_account()
        rollbar_token = config.get("ROLLBAR_SCRIPT_TOKEN")
        subprocess.run(
            f"docker run -e ENV=dev -e EE_SERVICE_ACCOUNT_JSON={service_account} -e ROLLBAR_SCRIPT_TOKEN={rollbar_token} --rm {dockerid} {param}",
            shell=True,
            check=True,
            cwd=tempdir,
        )
        return True
    except subprocess.CalledProcessError as error:
        logging.error(error)
        return False


def run(param, payload):
    """Start command"""
    logging.debug("Creating temporary file...")
    # Current folder
    cwd = os.getcwd()
    # Getting Dockerfile from /run folder
    dockerfile = os.path.dirname(os.path.realpath(__file__)) + "/run/Dockerfile"

    payload_data = {}
    if payload and payload != "":
        try:
            with open(payload) as data_file:
                payload_data = dict(json.load(data_file))
        except Exception as error:
            logging.error(error)
            return False

    with tempfile.TemporaryDirectory() as tmpdirname:
        logging.debug("Copying Dockerfile ...")
        copyfile(dockerfile, tmpdirname + "/Dockerfile")

        logging.debug("Copying src folder ...")
        copytree(cwd + "/src", tmpdirname + "/src")

        logging.debug("Copying requirements ...")
        copyfile(cwd + "/requirements.txt", tmpdirname + "/requirements.txt")

        logging.debug("Building ...")
        dockerid = "gef-local-" + str(time.time())
        success = False
        if build_docker(tmpdirname, dockerid):
            logging.debug("Reading and serializing parameters ....")
            param_dict = query_to_dict(param) if param != "" else {}
            param_dict.update(payload_data)
            param_serial = json.dumps(param_dict).encode("utf-8")
            param_serial = base64.b64encode(param_serial)
            logging.debug("Running script....")
            success = run_docker(tmpdirname, dockerid, param_serial)

        return success
