"""Login command"""

import re
from getpass import getpass

import requests

from tecli import config

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


def is_valid_email(email):
    """Check if the email is valid"""
    return bool(email) and EMAIL_REGEX.match(email)


def is_valid_password(password):
    """Check if the password is valid"""
    return bool(password)


def run():
    """Login command"""

    email = config.get("email")
    while email == "" or not is_valid_email(email):
        email = input("Please enter your email: ")

    password = config.get("password")
    while password is None or not is_valid_password(password):
        password = getpass(prompt="Please enter your password:")

    response = requests.post(
        url=config.get("url_api") + "/auth", json={"email": email, "password": password}
    )

    if response.status_code != 200:
        print("Error login.")
        return False

    body = response.json()

    config.set("JWT", body["access_token"])

    return True
