from flask import Flask
import os
import psycopg2

app = Flask(__name__)
port = int(os.getenv("PORT",3001))
counter = 0

POSTGRES_URL = os.getenv("POSTGRES_URL")

def connect_to_postgres():
    return psycopg2.connect(POSTGRES_URL)


def get_counter_from_db():
    conn = connect_to_postgres()
    curr = conn.cursor()
    curr.execute("SELECT count FROM counters WHERE id = 1;")
    count = curr.fetchone()
    curr.close()
    conn.close()
    return count[0]


def increment_counter():
    conn= connect_to_postgres()
    curr = conn.cursor()
    curr.execute("UPDATE counters SET count = count + 1 WHERE id = 1;")
    conn.commit()
    curr.close()
    conn.close()

#####
    
@app.get("/")
def pong():
    increment_counter()
    current_count = get_counter_from_db()
    return f"pong {current_count}"

@app.get("/pings")
def ping_count():
    counter = get_counter_from_db()
    return str(counter)

@app.get("/")
def root():
    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)























###when using txt files / volumes###
"""LOG_PATH = "/shared/pongcount.txt"

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
        f.write(str(value))"""