import uuid
import time
import os
import datetime
import logging

LOG_FILE_PATH = os.environ.get('LOG_FILE_PATH', 
                               "/tmp/log_output/random.log")

logger = logging.getLogger(__name__)

def main():
    logger.setLevel(logging.INFO)
    logger.info("Starting log writer")
    logger.info("Log file path: %s", LOG_FILE_PATH)
    
    log_uuid = str(uuid.uuid4())

    with open(LOG_FILE_PATH, "a") as log_file:
        while True:
            timestamp = str(datetime.datetime.now(datetime.UTC)) + "Z"
            log_file.write(f"{timestamp}: {log_uuid}\n")
            log_file.flush()
            time.sleep(5)

if __name__ == "__main__":
    main()