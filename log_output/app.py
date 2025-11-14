import time, uuid, datetime

value = str(uuid.uuid4())

while True:
	aika = datetime.datetime.utcnow().isoformat() + "Z"
	string = aika + ": " + value
	print(string, flush=True)
	time.sleep(5)


