"""Wrapper for the CLI commands."""

import logging
from datetime import timedelta

from termcolor import colored

from tecli import clear, config, create, download, info, login, logs, publish, start


class Commands:
    """GEF Command class Wrapper"""

    @staticmethod
    def create():
        """Create new project"""
        try:
            print("Creating the project")
            if create.run():
                print(colored("Project created successfully", "green"))
            else:
                print(colored("Project not created", "red"))
        except Exception as error:
            logging.error(error)

    @staticmethod
    def start(queryParams="", payload=""):
        """Start a script"""
        try:
            print("Running the script")
            if start.run(queryParams, payload):
                print(colored("Execution Finished", "green"))
            else:
                print(colored("Error running the script", "red"))
        except Exception as error:
            logging.error(error)

    @staticmethod
    def config(action, var_name, value=None):
        """Config GEE"""
        try:
            print("Configuring the script")
            if config.run(action, var_name, value):
                print(colored("Configuration done", "green"))
            else:
                print(colored("Error in the configuration", "red"))
        except Exception as error:
            logging.error(error)

    @staticmethod
    def login():
        """Log in the API"""
        try:
            print("Logging the user in")
            if login.run():
                print(colored("You are logged in", "green"))
            else:
                print(colored("Error with the user", "red"))
        except Exception as error:
            logging.error(error)

    @staticmethod
    def publish(public=False, overwrite=False):
        """Publish a script"""
        try:
            print("Publishing the script")
            if publish.run(public, overwrite):
                print(colored("Script published successfully", "green"))
            else:
                print(colored("Error publishing the script", "red"))
        except Exception as error:
            logging.error(error)

    @staticmethod
    def download(script_id=None):
        """Download a script"""
        try:
            print("Downloading the script")
            if download.run(script_id):
                print(colored("Script downloaded successfully", "green"))
            else:
                print(colored("Error downloading the script", "red"))
        except Exception as error:
            logging.error(error)

    @staticmethod
    def clear():
        """Clear docker trash"""
        try:
            print("Cleaning trash")
            if clear.run():
                print(colored("You are cleaned enough", "green"))
            else:
                print(colored("Error cleaning the system", "red"))
        except Exception as error:
            logging.error(error)

    @staticmethod
    def info():
        """Get info script"""
        try:
            print("Getting info script")
            if info.run():
                pass
            else:
                print(colored("Error getting info script", "red"))
        except Exception as error:
            logging.error(error)

    @staticmethod
    def logs(since=timedelta(hours=1)):
        """Get logs of script"""
        try:
            print("Getting logs of script build")
            if logs.run(since):
                pass
            else:
                print(colored("Error getting logs", "red"))
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as error:
            logging.error(error)
