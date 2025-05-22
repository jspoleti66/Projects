from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')
CORS(app)

DID_API_KEY = os.getenv("DID_API_KEY")
DID_BASE_URL = "https://api.d-id.com"

@app.route("/")
def index():
    return send_from_directory("templates", "index.html")

@app.route("/script.js")
def serve_script():
    return send_from_directory("static", "script.js")

@app.route("/start-stream", methods=["POST"])
def start_stream():
    url = f"{DID_BASE_URL}/talks/streams"
    headers = {
        "Authorization": f"Basic {DID_API_KEY}",
        "Content-Type": "application/json",
    }

    body = {
        "source_url": "https://raw.githubusercontent.com/jspoleti66/Projects/main/static/AlmostMe.png",
        "config": {
            "fluent": True,
            "pad_audio": 0.2,
        }
    }

    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 201:
        data = response.json()
        stream_id = data.get("id")
        stream_url = f"https://talks.d-id.com/stream/{stream_id}"
        return jsonify({"stream_url": stream_url})
    else:
        return jsonify({"error": response.text}), 500

if __name__ == "__main__":
    app.run(debug=True)
