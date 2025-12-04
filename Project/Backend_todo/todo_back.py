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


def init_db():
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Create table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id SERIAL PRIMARY KEY,
                content TEXT
            );
        """)

        # Add "done" column if it doesn't exist
        cur.execute("""
            ALTER TABLE todos
            ADD COLUMN IF NOT EXISTS done BOOLEAN DEFAULT FALSE;
        """)

        conn.commit()
        cur.close()
        conn.close()
        logging.info("Database initialized successfully.")
    except Exception as e:
        logging.error(f"Database initialization failed: {e}")



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

@app.get("/healthz")
def pod_ready():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.fetchone()
        cur.close()
        conn.close()
        return "OK", 200
    except:
        return "Couldn't open db", 500
    
@app.get("/livez")
def pod_alive():
    return "POD OK", 200

@app.get("/todos")
def transfer_todos():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT id, content, done FROM todos;")
    rows = cur.fetchall()

    todos = [
        {"id": r[0], "content": r[1], "done": r[2]}
        for r in rows
    ]

    cur.close()
    conn.close()
    return jsonify(todos)

@app.put("/todos/<int:id>")
def update_todo(id):
    data = request.get_json()
    # Validate input
    if "done" not in data:
        return "Missing 'done' field", 400

    done = data["done"]

    conn = get_connection()
    cur = conn.cursor()

    # Update the todo and return the updated row
    cur.execute("""
        UPDATE todos
        SET done = %s
        WHERE id = %s
        RETURNING id, content, done;
    """, (done, id))

    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if row is None:
        return "Todo not found", 404

    return jsonify({
        "id": row[0],
        "content": row[1],
        "done": row[2]
    })





if __name__ == "__main__":

    # Initialize DB at startup
    init_db()
    app.run(host="0.0.0.0", port=port)
