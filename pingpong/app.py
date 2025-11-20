from flask import Flask
import os

app = Flask(__name__)
port = int(os.getenv("PORT",3001))
counter = 0

###when using txt files / volumes###
LOG_PATH = "/shared/pongcount.txt"

def read_counter():
    if not os.path.exists(LOG_PATH):
        return 0
    with open(LOG_PATH, "r") as f:
        try:
            return int(f.read().strip())
        except:
            return 0

def write_counter(value):
    with open(LOG_PATH, "w") as f:
        f.write(str(value))
#####
        
### using endpoints 
@app.get("/pingpong")
def pong():
    global counter
    counter = counter + 1
    return f"pong {counter}"

@app.get("/pings")
def ping_count():
    return str(counter)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)

