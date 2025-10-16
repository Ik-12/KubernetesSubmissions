import os
import uuid
import time
import datetime
import threading
from flask import Flask

app = Flask(__name__)
log_uuid = str(uuid.uuid4())

def get_log_string():
    timestamp = str(datetime.datetime.now(datetime.UTC)) + "Z"
    return f"{timestamp}: {log_uuid}"

@app.route("/log")
def log_endpoint():
    return get_log_string()

def log_loop():
    while True:
        print(get_log_string())
        time.sleep(5)

if __name__ == "__main__":
    t = threading.Thread(target=log_loop, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
