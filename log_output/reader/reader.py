from flask import Flask
import os


app = Flask(__name__)
port = int(os.getenv("PORT",3000))
LOG_PATH = "/shared/log.txt"

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
            return lines[-1]
        return "no logs yet"
    except FileNotFoundError:
        return "log file not found"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)