from flask import Flask, jsonify, request, send_from_directory
import requests
import os

app = Flask(__name__, static_folder="static")

DID_API_KEY = os.environ.get("DID_API_KEY")
IMAGE_URL = "https://raw.githubusercontent.com/jspoleti66/Projects/main/static/AlmostMe.png"

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/api/init", methods=["POST"])
def init_stream():
    url = "https://api.d-id.com/talks/streams"
    headers = {
        "Authorization": f"Basic {DID_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"source_url": IMAGE_URL}
    response = requests.post(url, json=payload, headers=headers)

    try:
        data = response.json()
        print("API Response:", data)
        return jsonify({
            "streamId": data.get("id"),
            "token": data.get("token")
        })
    except Exception as e:
        print("Error decoding JSON:", response.text)
        return jsonify({"error": "Failed to init stream"}), 500

@app.route("/static/<path:path>")
def serve_static(path):
    return send_from_directory("static", path)
