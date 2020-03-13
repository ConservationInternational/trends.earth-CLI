
"""Logs command"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from termcolor import colored
from datetime import datetime

import dateutil.parser
import os
import logging
import json
import requests
import time


from tecli import config

def read_jwt_token():
    """Obtain logs token of config user"""
    return config.get('JWT')

def read_configuration():
    """Read configuration file of project"""
    to_dir = os.getcwd()
    logging.debug('Reading configuration file in path: %s' % (to_dir))
    with open(os.path.join(to_dir, 'configuration.json'), 'r') as json_data:
        d = json.load(json_data)
        return d

def get_logs(script, last_date):
    """Get logs from server"""
    logging.debug('Obtaining logs')
    token = read_jwt_token()
    start_query = ''
    if last_date:
        start_query = '?start=' +  last_date.isoformat()

    response = requests.get(url=config.get('url_api') + '/api/v1/script/' + script['id'] + '/log' + start_query,
                            headers={'Authorization': 'Bearer ' + token})
    if response.status_code != 200:
        if response.status_code == 401:
            print(colored('Do you need login', 'red'))
        else:
            print(colored('Error obtaining logs of script.', 'red'))
        return False, None
    return True, response.json()['data']

def show_logs(script):
    """Show logs in console"""
    last_date = None
    for log in script['logs']:
        last_date = dateutil.parser.parse(log['register_date'])
        if log['text'] != None:
            print(log['register_date'] + ': ' + log['text'])

    if script['status'] != 'FAIL' and script['status'] != 'SUCCESS':
        next = True
        while next == True:
            next, logs = get_logs(script, last_date)
            if logs:
                for log in logs:
                    last_date = dateutil.parser.parse(log['register_date'])
                    if log['text'] != None:
                        print(log['register_date'] + ': ' + log['text'])
            time.sleep(2)



def run():
    """Run command"""
    try:
        configuration = read_configuration()
        if 'id' not in configuration:
            print(colored('Script NOT PUBLISHED', 'red'))
            return True

        else:
            token = read_jwt_token()
            response = requests.get(url=config.get('url_api') + '/api/v1/script/' + configuration['id'], headers={'Authorization': 'Bearer ' + token})
            if response.status_code != 200:
                if response.status_code == 401:
                    print(colored('Do you need login', 'red'))
                else:
                    print(colored('Error obtaining info of script.', 'red'))
                return False
            script = response.json()

            show_logs(script['data'])

    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as error:
        logging.error(error)
        return False

    return True
