"""Logs command"""

from __future__ import absolute_import, division, print_function

import json
import logging
import os
import time
from datetime import datetime, timedelta

import dateutil.parser
import pytz
import requests
from termcolor import colored

from tecli import config


def read_jwt_token():
    """Obtain logs token of config user"""
    return config.get("JWT")


def read_configuration():
    """Read configuration file of project"""
    to_dir = os.getcwd()
    logging.debug("Reading configuration file in path: %s" % (to_dir))
    with open(os.path.join(to_dir, "configuration.json"), "r") as json_data:
        d = json.load(json_data)
        return d


def get_logs(script, last_date):
    """Get logs from server"""
    logging.debug("Obtaining logs")
    token = read_jwt_token()
    start_query = ""
    if last_date:
        start_query = "?start=" + last_date.isoformat()
    response = requests.get(
        url=config.get("url_api")
        + "/api/v1/script/"
        + script["id"]
        + "/log"
        + start_query,
        headers={"Authorization": "Bearer " + token},
    )
    if response.status_code != 200:
        if response.status_code == 401:
            print(colored("Do you need login", "red"))
        else:
            print(colored("Error obtaining logs of script.", "red"))
        return False, None
    return True, response.json()["data"]


def show_logs(script, since):
    """Show logs in console"""
    last_date = None
    now = datetime.utcnow().replace(tzinfo=pytz.utc)
    printed = False
    for log in script["logs"]:
        last_date = dateutil.parser.parse(log["register_date"]).replace(tzinfo=pytz.utc)
        if log["text"] is not None and (last_date > (now - since)):
            print(log["register_date"] + ": " + log["text"])
            printed = True

    if not printed:
        print(f"No log entries in last {since}")

    # Below will sleep and keep printing logs during script build

    if script["status"] != "FAIL" and script["status"] != "SUCCESS":
        next = True
        while next:
            next, logs = get_logs(script, last_date)
            if logs:
                for log in logs:
                    last_date = dateutil.parser.parse(log["register_date"])
                    if log["text"] is not None:
                        print(log["register_date"] + ": " + log["text"])

            time.sleep(2)


def run(since=timedelta(hours=1)):
    """Run command"""
    try:
        configuration = read_configuration()
        if "id" not in configuration:
            print(colored("Script NOT PUBLISHED", "red"))
            return True

        else:
            token = read_jwt_token()
            response = requests.get(
                url=config.get("url_api")
                + f"/api/v1/script/{configuration['id']}?include=logs",
                headers={"Authorization": "Bearer " + token},
            )
            if response.status_code != 200:
                if response.status_code == 401:
                    print(colored("Do you need login", "red"))
                else:
                    print(colored("Error obtaining info of script.", "red"))
                return False
            script = response.json()
            if not isinstance(since, timedelta):
                since = timedelta(hours=since)

            show_logs(script["data"], since)

    except (KeyboardInterrupt, SystemExit):
        raise

    except Exception as error:
        logging.error(error)
        return False

    return True
