import os
import logging
from flask import Flask

LOG_FILE_PATH = os.environ.get('LOG_FILE_PATH', 
                               "/tmp/log_output/random.log")

PONG_COUNT_FILE_PATH = os.environ.get('PONG_COUNT_FILE_PATH', 
                                    '/tmp/pong_log/pong_count')

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

def get_log_string():
    try:
        with open(LOG_FILE_PATH, "r") as f:
            log = f.read()
    except Exception as e:
        return f"Error reading log file: {e}"
    
    try:
        with open(PONG_COUNT_FILE_PATH, "r") as f:
            pong_count = f.read()
    except Exception as e:
        return f"Error reading pong count file: {e}"
    
    resp = log + f"Ping / Pongs: {pong_count}"
    
    return resp

@app.route("/log")
def log_endpoint():
    return get_log_string()

if __name__ == "__main__":
    app.logger.info("Starting log reader API")
    app.logger.info("Log file path: %s", LOG_FILE_PATH)
    app.logger.info("Pong count file path: %s", PONG_COUNT_FILE_PATH)

    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
