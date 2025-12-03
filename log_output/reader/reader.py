from flask import Flask
import os
import requests

app = Flask(__name__)
port = int(os.getenv("PORT",3000))
LOG_PATH = "/shared/log.txt"
#LOG_PATH_PONG = "/shared/pongcount.txt"
PINGPONG_URL = "http://pingpong-svc:3456/pings" 

@app.get("/status")
def file_read():
    #### read the whole log-file if not found raise error
    try:
        with open(LOG_PATH, "r") as f:
            lines = f.read()
        return f"<pre>{lines}</pre>"
    except FileNotFoundError:
        return "File not found :("
    
@app.get("/")
def status():
    try:
        with open(LOG_PATH, "r") as f:
            lines = f.readlines()
        last_log = lines[-1].strip() if lines else "No logs yet"
    except FileNotFoundError:
        last_log = "Log file not found"

    try: 
        response = requests.get(PINGPONG_URL)
        pong_count = response.text
    except:
        pong_count = "0"

    message = os.getenv("MESSAGE", "nothing found")

    try:
        with open("/etc/config/information.txt", "r") as f:
            file_content = f.read().strip()
    except FileNotFoundError:
        file_content = "File not found"

    return (
        f"file content: {file_content}\n"
        f"env variable: MESSAGE={message}\n"
        f"{last_log}\n"
        f"Ping / Pongs: {pong_count}"
    )

@app.get("/healthz")
def get_health():
    try:
        response = requests.get(PINGPONG_URL)
        status_code = response.status_code
        if status_code == 200:
            return "OK", 200
        else:
            return "Pingpong is not ready", 500
    except:
        return "pingpong not reachable", 500
    

@app.get("/debug-check")
def debug_check():
    return "You are hitting the reader container!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)