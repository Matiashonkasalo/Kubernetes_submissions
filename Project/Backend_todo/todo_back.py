from flask import Flask, request, jsonify
import os
import psycopg2
import logging

logging.basicConfig(level=logging.INFO)

port = int(os.getenv("PORT", 3002))
app = Flask(__name__)

print(f"Backend server running on {port}")

POSTGRES_URL = os.getenv("POSTGRES_URL")


def get_connection():
    return psycopg2.connect(POSTGRES_URL)


#### create db and check if there exists todo table 
def init_db():
    """Create the todos table if it does not exist."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id SERIAL PRIMARY KEY,
                content TEXT
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        logging.info("Database initialized successfully.")
    except Exception as e:
        logging.error(f"Database initialization failed: {e}")

# Initialize DB at startup
init_db()


##receiving a new todo and updating the list
@app.post("/todos")
def getting_todos():
    data = request.get_json() 
    if not data or "content" not in data:
        logging.warning("Todo is rejected (content not found)")
        return "Missing todo content", 400
    
    content = data["content"]
    logging.info(f"Received todo: {content}")

    if len(content) > 140:
        logging.warning(f"Todo rejected (too long): length={len(content)}")
        return "Todo too long", 400
    conn = get_connection()
    curr = conn.cursor()
    curr.execute("INSERT INTO todos (content) VALUES (%s)", (content,))
    conn.commit()
    curr.close()
    conn.close()
    return "OK", 200

#tranfering the todos back to front
@app.get("/todos")
def transfer_todos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT content FROM todos;")
    rows = cur.fetchall()
    todos = [r[0] for r in rows]
    cur.close()
    conn.close()
    return jsonify(todos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
