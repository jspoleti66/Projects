from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)

DID_API_KEY = os.getenv("DID_API_KEY")
DID_BASE_URL = "https://api.d-id.com"

headers = {
    "Authorization": f"Bearer {DID_API_KEY}",
    "Content-Type": "application/json",
}

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/script.js")
def serve_script():
    return send_from_directory(".", "script.js")

@app.route("/start-stream", methods=["POST"])
def start_stream():
    url = f"{DID_BASE_URL}/talks/streams"
    body = {
        "source_url": "https://raw.githubusercontent.com/jspoleti66/Projects/main/static/AlmostMe.png",
        "driver_url": None,
        "config": {
            "fluent": True,
            "pad_audio": 0.2,
        }
    }

    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 201:
        data = response.json()
        stream_id = data.get("id")
        return jsonify({"stream_id": stream_id})
    else:
        return jsonify({"error": response.text}), 500

@app.route("/webrtc-offer/<stream_id>", methods=["POST"])
def webrtc_offer(stream_id):
    data = request.json
    sdp_offer = data.get("sdpOffer")
    if not sdp_offer:
        return jsonify({"error": "No SDP offer received"}), 400

    url = f"{DID_BASE_URL}/talks/streams/{stream_id}/webrtc-offer"
    payload = {
        "sdpOffer": sdp_offer
    }
    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code == 201:
        answer = resp.json().get("sdpAnswer")
        return jsonify({"sdpAnswer": answer})
    else:
        return jsonify({"error": resp.text}), 500

if __name__ == "__main__":
    app.run(debug=True)
