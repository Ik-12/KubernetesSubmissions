import os
import logging
from flask import Flask
import requests

LOG_FILE_PATH = os.environ.get('LOG_FILE_PATH', 
                               "/tmp/log_output/random.log")

INFO_FILE_PATH = os.environ.get('INFO_FILE_PATH', 
                               "/tmp/information.txt")

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
    try:
        response = requests.get(PONG_COUNT_SERVICE_URL, timeout=3)
        response.raise_for_status()
        pings_resp = response.json()
        app.logger.debug("/pings response: %s", pings_resp if 'pings_resp' in locals() else "No response")

        pong_count = pings_resp.get('pong_count', 'N/A')
    except Exception as e:
        app.logger.error("Error calling pong-count service: %s", e)
        pong_count = "Error getting pong count"
    
    resp = log + f"Ping / Pongs: {pong_count}"
    
    # Include the MESSAGE environment variable and file content from
    # config map
    resp = f"env variable: MESSAGE={os.getenv("MESSAGE")}" + "\n" \
        + "file content:" + open(INFO_FILE_PATH, "r").read() + "\n" \
        + resp
    
    return resp

@app.route("/log")
def log_endpoint():
    return get_log_string()

if __name__ == "__main__":
    app.logger.info("Starting log reader API")
    app.logger.info("Log file path: %s", LOG_FILE_PATH)
    app.logger.info("Pong count API URL: %s", PONG_COUNT_SERVICE_URL)

    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
