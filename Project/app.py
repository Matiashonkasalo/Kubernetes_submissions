from flask import Flask, send_file, render_template
import requests
import time
import os

app = Flask(__name__)

#reading port using environmental variable

port = int(os.getenv("PORT",8000))
MAX_AGE = 600
CACHE_IMAGE = "/shared/image.jpg"
CACHE_TIMESTAMP = "/shared/timestamp.txt"
print(f"Server started in port {port}")

def valid_cache():

    ### checking if the paths exists 
    if not os.path.exists(CACHE_IMAGE):
        return False
    if not os.path.exists(CACHE_TIMESTAMP):
        return False
    ### Reading the timestamp and returning true if the image hasn't been up 10 mins
    try:
        with open(CACHE_TIMESTAMP,"r") as f:
            ts = float(f.read().strip())
    except:
        return False
    return (time.time() - ts) < MAX_AGE

def update_image():
    ### get image and write its content to file
    response = requests.get("https://picsum.photos/1200")
    with open(CACHE_IMAGE, "wb") as f:
        f.write(response.content)
    ### start the timer 
    with open(CACHE_TIMESTAMP, "w") as f:
        f.write(str(time.time()))

@app.get("/")
def home():
    ###cheking how long the image been up if more than 10 mins update
    if not valid_cache():
        print("Cache expired -> fetching new image")
        update_image()
    return render_template("index.html")


@app.get("/image")
def image():
    return send_file(CACHE_IMAGE, mimetype="image/jpeg")

    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
