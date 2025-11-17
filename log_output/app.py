import time, uuid, datetime
from flask import Flask
import os
import threading

value = str(uuid.uuid4())

app = Flask(__name__)
port = int(os.getenv("PORT",3000))

def print_logs():
	while True:
		aika = datetime.datetime.utcnow().isoformat() + "Z"
		string = aika + ": " + value
		print(string, flush=True)
		time.sleep(5)


@app.get("/status")
def status():
    aika = datetime.datetime.utcnow().isoformat() + "Z"
    return f"{aika}: {value}"
      
if __name__ == "__main__":
    threading.Thread(target=print_logs, daemon=True).start()
    app.run(host="0.0.0.0", port=port)

	
	