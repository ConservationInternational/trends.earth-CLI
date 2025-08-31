"""Download command"""

import logging
import tarfile

import requests
from termcolor import colored

from tecli import config


def read_jwt_token():
    """Obtain logs token of config user"""
    return config.get("JWT")


def run(script_id=None):
    """Download command"""
    if not script_id:
        logging.error("invalid script_id")
        return False
    try:
        token = read_jwt_token()
        response = requests.get(
            url=config.get("url_api") + "/api/v1/script/" + script_id + "/download",
            headers={"Authorization": "Bearer " + token},
            stream=True,
        )
        if response.status_code != 200:
            if response.status_code == 401:
                print(colored("Do you need login", "red"))
            else:
                print(colored("Error obtaining info of script.", "red"))
            return False
            # path = os.getcwd() + '/' + configuration.get('id')
        tar = tarfile.open(mode="r:gz", fileobj=response.raw)
        tar.extractall(path="./" + script_id)

    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as error:
        logging.error(error)
        return False

    return True
