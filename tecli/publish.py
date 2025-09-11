"""Publish command"""

import json
import logging
import os
import tarfile

from termcolor import colored

from tecli import auth, config


def make_tarfile(name):
    """Create tar.gz file with the content of the directory"""
    to_dir = os.getcwd()
    makefile = os.path.join(to_dir, name + ".tar.gz")
    logging.debug(f"Creating tar.gz file in path: {to_dir}")
    with tarfile.open(makefile, "w:gz") as tar:
        tar.add(to_dir + "/configuration.json", arcname="configuration.json")
        tar.add(to_dir + "/requirements.txt", arcname="requirements.txt")
        tar.add(to_dir + "/src", arcname="src")
        return makefile


def read_configuration():
    """Read configuration file of project"""
    to_dir = os.getcwd()
    logging.debug(f"Reading configuration file in path: {to_dir}")
    with open(os.path.join(to_dir, "configuration.json")) as json_data:
        d = json.load(json_data)
        return d


def write_configuration(data):
    """Write configuration file"""
    to_dir = os.getcwd()
    logging.debug(f"Writing configuration file in path: {to_dir}")
    with open(os.path.join(to_dir, "configuration.json"), "w") as config_file:
        json.dump(data, config_file)


def sure_overwrite():
    sure = None

    while sure is None or not bool(sure) or sure.lower() not in ["y", "n"]:
        sure = input("With this action you will overwrite this script. Are you sure? (Y/n): ")
        if sure == "":
            sure = "y"

    return sure == "y" or sure == "Y"


def publish(public=False, overwrite=False):
    """Publish script in API"""
    tarfile = None
    try:
        configuration = read_configuration()
        if "name" not in configuration:
            print("Name required in configuration file")
            return False
        tarfile = make_tarfile(configuration["name"])
        logging.debug(f"Doing request with file {tarfile}")

        response = None
        if "id" in configuration:
            if overwrite:
                sure = True
            else:
                sure = sure_overwrite()

            if not sure:
                return False

            # Use authenticated request for PATCH
            with open(tarfile, "rb") as f:
                response = auth.make_authenticated_request(
                    "PATCH",
                    config.get("url_api") + "/api/v1/script/" + configuration["id"],
                    files={"file": f},
                )
        else:
            # Use authenticated request for POST
            with open(tarfile, "rb") as f:
                response = auth.make_authenticated_request(
                    "POST", config.get("url_api") + "/api/v1/script", files={"file": f}
                )

        if response is None:
            print(colored("Authentication failed. Please login.", "red"))
            return False

        if response.status_code != 200:
            logging.error(response.json())
            if response.status_code == 401:
                print(colored("Do you need to login?", "red"))
            else:
                print(colored("Error publishing script.", "red"))
            return False

        data = response.json()
        configuration["id"] = data["data"]["id"]
        write_configuration(configuration)
        if public:
            response = auth.make_authenticated_request(
                "POST", config.get("url_api") + "/api/v1/script/" + configuration["id"] + "/publish"
            )

            if response is None:
                print(colored("Authentication failed. Please login.", "red"))
                return False

            if response.status_code != 200:
                logging.error(response.json())
                print(colored("Error making the script public.", "red"))
                return False
        return True
    except OSError:
        print(colored("Execute this command in a GEF project", "red"))
        return False
    finally:
        if tarfile:
            os.remove(path=tarfile)


def run(public=False, overwrite=False):
    """Publish command"""
    return publish(public, overwrite)
