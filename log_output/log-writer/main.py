import uuid
import time
import datetime

LOG_FILE_PATH = "/tmp/random.log"

def main():
    log_uuid = str(uuid.uuid4())

    with open(LOG_FILE_PATH, "a") as log_file:
        while True:
            timestamp = str(datetime.datetime.now(datetime.UTC)) + "Z"
            log_file.write(f"{timestamp}: {log_uuid}\n")
            log_file.flush()
            time.sleep(5)

if __name__ == "__main__":
    main()