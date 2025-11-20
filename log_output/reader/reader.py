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

    ## 1) open the log-file and read the current status
    try:
        with open(LOG_PATH, "r") as f:
            lines = f.readlines()
        if lines:
            last_log = lines[-1].strip()
        else:
            last_log = "No logs yet"
    except FileNotFoundError:
        return "Log file not found"
    
    ### 2) fetch the data over http

    try: 
        response = requests.get(PINGPONG_URL)
        pong_count = response.text
    except:
        pong_count = "0"
    
    return f"{last_log} \n Ping / Pongs: {pong_count}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)