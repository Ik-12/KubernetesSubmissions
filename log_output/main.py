import uuid
import time
import datetime

def main():
    log_uuid = str(uuid.uuid4())

    while True:
        timestamp = str(datetime.datetime.now(datetime.UTC)) + "Z"
        print(f"{timestamp}: {log_uuid}")

        time.sleep(5)

if __name__ == "__main__":
    main()
