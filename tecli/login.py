"""Login command"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from getpass import getpass
from tecli.configuration import SETTINGS

from tecli import config

import re
import requests

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


def is_valid_email(email):
    """Check if the email is valid"""
    return bool(email) and EMAIL_REGEX.match(email)

def is_valid_password(password):
    """Check if the password is valid"""
    return bool(password)

def run():
    """Login command"""

    email = None
    while email is None or not is_valid_email(email):
        email = input("Please enter your email: ")

    password = None
    while email is None or not is_valid_password(password):
        password = getpass(prompt='Please enter your password:')


    response = requests.post(url=SETTINGS.get('url_api')+'/auth', json={'email': email, 'password': password})

    if response.status_code != 200:
        print('Error login.')
        return False

    body = response.json()

    config.set('JWT', body['access_token'])

    return True
