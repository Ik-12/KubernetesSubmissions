import os
import logging
from flask import Flask
import requests

LOG_FILE_PATH = os.environ.get('LOG_FILE_PATH', 
                               "/tmp/log_output/random.log")

PONG_COUNT_SERVICE_URL = os.environ.get('PONG_COUNT_SERVICE_URL',
                                      "http://127.0.0.1:1122/pings")

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

def get_log_string():
    # Read the log file
    try:
        with open(LOG_FILE_PATH, "r") as f:
            log = f.read()
    except Exception as e:
        return f"Error reading log file: {e}"
    
    # Call the /pings endpoint of the pong-count service
    pings_resp = requests.get(PONG_COUNT_SERVICE_URL).json()
    app.logger.debug("/pings response: %s", pings_resp)

    resp = log + f"Ping / Pongs: {pings_resp['pong_count']}"
    
    return resp

@app.route("/log")
def log_endpoint():
    return get_log_string()

if __name__ == "__main__":
    app.logger.info("Starting log reader API")
    app.logger.info("Log file path: %s", LOG_FILE_PATH)
    app.logger.info("Pong count API URL: %s", PONG_COUNT_SERVICE_URL)

    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
