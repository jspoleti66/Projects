from flask import Flask, render_template, jsonify
import requests
import os

app = Flask(__name__)

DID_API_KEY = os.getenv("DID_API_KEY")
AVATAR_URL = "https://raw.githubusercontent.com/jspoleti66/Projects/main/static/AlmostMe.png"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start-stream")
def start_stream():
    headers = {
        "Authorization": f"Basic {DID_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "source_url": AVATAR_URL
    }
    response = requests.post("https://api.d-id.com/talks/streams", json=body, headers=headers)
    data = response.json()
    return jsonify({
        "session_id": data.get("id"),
        "session_token": data.get("token"),
        "stream_url": data.get("stream_url")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))