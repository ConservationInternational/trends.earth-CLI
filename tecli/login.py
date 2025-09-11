"""Login command"""

import re
from datetime import datetime, timedelta
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

    # Store access token
    config.set("JWT", body["access_token"])

    # Store refresh token if provided
    if "refresh_token" in body:
        config.set("refresh_token", body["refresh_token"])

    # Store token expiration if provided
    if "expires_in" in body:
        expires_at = datetime.now() + timedelta(seconds=body["expires_in"])
        config.set("token_expires_at", expires_at.isoformat())

    print("Login successful!")
    return True
