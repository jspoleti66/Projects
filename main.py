from flask import Flask, request, jsonify, send_from_directory
import requests
import time
import os

app = Flask(__name__)

D_ID_API_KEY = os.getenv("D_ID_API_KEY")
TALK_IMAGE_URL = os.getenv("TALK_IMAGE_URL")
VOICE_ID = os.getenv("VOICE_ID", "en-US-Wavenet-F")
SOURCE_IMAGE_URL = TALK_IMAGE_URL or "https://raw.githubusercontent.com/jspoleti66/Projects/main/static/AlmostMe.png"

headers = {
    "Authorization": f"Bearer {D_ID_API_KEY}",
    "Content-Type": "application/json"
}

@app.route("/start-stream", methods=["POST"])
def start_stream():
    payload = {
        "source_url": SOURCE_IMAGE_URL,
        "config": {
            "fluent": True,
            "driver_expressions": {
                "expressions": [
                    {"start_frame": 0, "expression": "neutral", "intensity": 0}
                ]
            },
            "result_format": "webm",
            "stitch": True,
            "output_resolution": 512
        },
        "enable_streaming": True
    }
    res = requests.post("https://api.d-id.com/talks", headers=headers, json=payload)
    if res.status_code != 200:
        return jsonify({"error": res.text}), res.status_code

    talk = res.json()
    talk_id = talk.get("id")

    # Polling until talk status is "created"
    for _ in range(10):
        status_res = requests.get(f"https://api.d-id.com/talks/{talk_id}", headers=headers)
        status = status_res.json().get("status")
        if status == "created":
            return jsonify({"talk_id": talk_id})
        time.sleep(1)

    return jsonify({"error": "Timeout waiting for talk to be created."}), 504

@app.route("/webrtc-offer/<talk_id>", methods=["POST"])
def handle_offer(talk_id):
    offer = request.json.get("sdp")
    if not offer:
        return jsonify({"error": "No SDP offer"}), 400

    response = requests.post(
        f"https://api.d-id.com/talks/streams/{talk_id}/sdp-offer",
        headers=headers,
        json={"sdp": offer}
    )
    if response.status_code != 200:
        return jsonify({"error": response.text}), response.status_code

    return jsonify(response.json())

@app.route("/")
def serve_index():
    return send_from_directory(".", "index.html")

@app.route("/script.js")
def serve_script():
    return send_from_directory(".", "script.js")

if __name__ == "__main__":
    app.run(debug=True)
