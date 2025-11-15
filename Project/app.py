from flask import Flask

import os

app = Flask(__name__)

#reading port using environmental variable

port = int(os.getenv("PORT",8000))

print(f"Server started in port {port}]")

@app.get("/")
def root():
    return "Hello!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
