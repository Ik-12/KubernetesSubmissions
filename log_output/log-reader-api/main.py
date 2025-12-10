import logging
import os

import requests
from flask import Flask

LOG_FILE_PATH = os.environ.get("LOG_FILE_PATH", "/tmp/log_output/random.log")

INFO_FILE_PATH = os.environ.get("INFO_FILE_PATH", "/tmp/information.txt")

PONG_COUNT_SERVICE_URL = os.environ.get(
    "PONG_COUNT_SERVICE_URL", "http://127.0.0.1:1122/pings"
)

GREETER_URL = os.environ.get(
    "GREETER_URL", "http://localhost:5008/")

app = Flask(__name__)
app.logger.setLevel(logging.INFO)


def get_log_string():
    # Read the log file
    try:
        with open(LOG_FILE_PATH, "r") as f:
            log = f.read()
    except Exception as e:
        log = f"Error reading log file {LOG_FILE_PATH}: {e}"

    # Call the /pings endpoint of the pong-count service
    try:
        response = requests.get(PONG_COUNT_SERVICE_URL, timeout=3)
        response.raise_for_status()
        pings_resp = response.json()

        app.logger.debug(
            "/pings response: %s",
            pings_resp if "pings_resp" in locals() else "No response",
        )

        pong_count = pings_resp.get("pong_count", "N/A")
    except Exception as e:
        app.logger.error("Error calling pong-count service: %s", e)
        pong_count = f"Error getting pong count from {PONG_COUNT_SERVICE_URL}"

    try:
        greeting_response = requests.get(GREETER_URL, timeout=3)
        greetings = greeting_response.text
    except Exception as e:
        app.logger.error("Error calling greeter service: %s", e)
        greetings = f"Error getting greeting from {GREETER_URL}"

    resp = log + f"Ping / Pongs: {pong_count}" + f"\ngreetings: {greetings}\n"

    # Include the MESSAGE environment variable and file content from
    # config map
    resp = resp + f"env variable: MESSAGE={os.getenv('MESSAGE')}" + "\n"

    if os.path.exists(INFO_FILE_PATH):
        resp = resp 
        + "file content:"
        + open(INFO_FILE_PATH, "r").read()
        + "\n"
    else:
        resp = resp + f"Info file {INFO_FILE_PATH} does not exist.\n" 

    return resp


@app.route("/log")
def log_endpoint():
    return get_log_string()


@app.route("/")
def root():
    return "OK", 200


@app.route("/ready")
def ready():
    try:
        response = requests.get(PONG_COUNT_SERVICE_URL, timeout=3)
        response.raise_for_status()
    except Exception as e:
        return "Service Unavailable", 503

    return "OK", 200

if __name__ == "__main__":
    app.logger.info("Starting log reader API")
    app.logger.info("Log file path: %s", LOG_FILE_PATH)
    app.logger.info("Pong count API URL: %s", PONG_COUNT_SERVICE_URL)

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5010)))
