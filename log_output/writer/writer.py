import time, uuid, datetime

LOG_PATH = "/shared/log.txt"

value = str(uuid.uuid4())
while True:
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    with open(LOG_PATH, "a") as f:
        f.write(f"{timestamp}: {value}\n")
    time.sleep(5)

	
