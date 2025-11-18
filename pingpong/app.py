from flask import Flask
import os


app = Flask(__name__)

port = int(os.getenv("PORT",3001))
counter = 0

@app.get("/pingpong")
def pong():
    global counter
    counter = counter + 1
    return f"pong {counter}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)

