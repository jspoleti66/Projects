from flask import Flask, render_template, jsonify
import requests
import os

app = Flask(__name__)

DID_API_KEY = os.getenv("DID_API_KEY")
AVATAR_URL = "https://raw.githubusercontent.com/jspoleti66/Projects/main/static/AlmostMe.png"  # o el que estés usando

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start-stream", methods=["POST"])
def start_stream():
    headers = {
        "Authorization": f"Basic {DID_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "source_url": AVATAR_URL,
        "config": {"fluent": True}
    }
    response = requests.post("https://api.d-id.com/talks/streams", headers=headers, json=payload)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
