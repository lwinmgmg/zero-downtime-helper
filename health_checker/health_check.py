import os
import time
import requests
import logging

_loger = logging.getLogger(__name__)

TIMEOUT='TIMEOUT'
REQUEST_URL='REQUEST_URL'
SLEEP_DURATION='SLEEP_DURATION'


class Envs:
    def __init__(self):
        self.timeout = int(os.environ.get(TIMEOUT) or 20)
        self.url = os.environ.get(REQUEST_URL)
        self.sleep_duration = int(os.environ.get(SLEEP_DURATION) or 1)
    def validate(self):
        if not self.url:
            raise Exception("REQUEST_URL environment variable is required")


env = Envs()

def main():
    env.validate()
    old_time = time.time()
    response = None
    err = None

    while time.time() - old_time < env.timeout:
        try:
            response = requests.get(env.url, timeout=1)
            if response.status_code == 404 or response.status_code == 200:
                _loger.info("Successfully connected to the server", response.status_code)
                exit(0)
        except Exception as error:
            _loger.warning("Connecting to the server %s", env.url)
            if response:
                _loger.warning("Response status is %s", response.status_code)
            time.sleep(env.sleep_duration)
            err = error
    _loger.error("Error on connecting the server : %s", err)
    exit(1)

if __name__ == "__main__":
    main()
