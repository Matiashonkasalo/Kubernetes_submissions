from flask import Flask, request, jsonify
import os

port = int(os.getenv("PORT", 3002))
app = Flask(__name__)

print(f"Backend server running on {port}")
##apista klick -> tänne appedn list

list_of_todos = []

##receiving new a new todo and updating the list
@app.post("/todos")
def getting_todos():
    data = request.get_json() 
    if not data or "content" not in data:
        return "Missing todo content", 400
    content = data["content"]
    if len(content)>140:
        return "Todo is over 140 characters, try again"
    
    list_of_todos.append(content)
    return "OK", 200

#tranfering the todos back to front
@app.get("/todos")
def transfer_todos():
    return jsonify(list_of_todos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
