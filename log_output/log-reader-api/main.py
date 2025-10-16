import os
from flask import Flask

LOG_FILE_PATH = os.environ.get('LOG_FILE_PATH', 
                               "/tmp/log_output/random.log")

app = Flask(__name__)

def get_log_string():
    try:
        with open(LOG_FILE_PATH, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading log file: {e}"

@app.route("/log")
def log_endpoint():
    return get_log_string()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
