"""Info command"""

import json
import logging
import os

from termcolor import colored

from tecli import auth, config


def read_configuration():
    """Read configuration file of project"""
    to_dir = os.getcwd()
    logging.debug(f"Reading configuration file in path: {to_dir}")
    with open(os.path.join(to_dir, "configuration.json")) as json_data:
        d = json.load(json_data)
        return d


def run():
    try:
        configuration = read_configuration()
        if "id" not in configuration:
            print("Name: " + configuration["name"])
            print("Status: NOT PUBLISHED")

        else:
            # Use the new authenticated request function
            response = auth.make_authenticated_request(
                "GET", config.get("url_api") + "/api/v1/script/" + configuration["id"]
            )

            if response is None:
                print(colored("Authentication failed. Please login.", "red"))
                return False

            if response.status_code != 200:
                if response.status_code == 401:
                    print(colored("Do you need login", "red"))
                else:
                    print(colored("Error obtaining info of script.", "red"))
                return False
            else:
                data = response.json()
                print("Id: " + data["data"]["id"])
                print("Slug: " + data["data"]["name"])
                print("Name: " + data["data"]["slug"])
                print("Status: " + data["data"]["status"])
                print("CreatedAt: " + data["data"]["created_at"])
                print(
                    "Run script: "
                    + config.get("url_api")
                    + "/api/v1/script/"
                    + data["data"]["name"]
                    + "/run?params"
                )

    except Exception as error:
        logging.error(error)
        return False

    return True
