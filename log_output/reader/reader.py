from flask import Flask
import os

app = Flask(__name__)
port = int(os.getenv("PORT",3000))
LOG_PATH = "/shared/log.txt"
LOG_PATH_PONG = "/shared/pongcount.txt"

@app.get("/")
def file_read():
    try:
        with open(LOG_PATH, "r") as f:
            lines = f.read()
        return f"<pre>{lines}</pre>"
    except FileNotFoundError:
        return "File not found :("
    
@app.get("/status")
def status():
    try:
        with open(LOG_PATH, "r") as f:
            lines = f.readlines()
        if lines:
            last_log = lines[-1].strip()
        else:
            last_log = "No logs yet"
    except FileNotFoundError:
        return "Log file not found"
    try:
        with open(LOG_PATH_PONG,"r") as f:
            pong_count = f.read().strip()
        if pong_count == "":
            pong_count = "0"
    except:
        pong_count = "0"

    return f"{last_log} \n Ping / Pongs: {pong_count}"
        

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)