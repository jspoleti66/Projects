from flask import Flask, request, jsonify, send_from_directory
import requests
import os

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
DID_API_KEY = os.getenv("DID_API_KEY")  # clave segura

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/script.js")
def script():
    return send_from_directory(".", "script.js")

@app.route("/create_stream", methods=["POST"])
def create_stream():
    user_text = request.json.get("text", "Hola, soy tu clon AlmostMe")

    headers = {
        "Authorization": f"Bearer {DID_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "source_url": "https://raw.githubusercontent.com/jspoleti66/Projects/main/static/AlmostMe.png",
        "config": {
            "stitch": True,
            "driver_expressions": {
                "expressions": [
                    {"expression": "happy", "start_frame": 0, "intensity": 0.4}
                ]
            },
        },
        "script": {
            "type": "text",
            "input": user_text,
            "provider": {"type": "microsoft", "voice_id": "es-ES-AlvaroNeural"},
            "ssml": False
        }
    }

    response = requests.post("https://api.d-id.com/talks/streams", headers=headers, json=body)
    data = response.json()

    stream_id = data.get("id")
    sdp_offer = data.get("offer")
    ice_servers = data.get("ice_servers")

    return jsonify({
        "streamId": stream_id,
        "sdp": sdp_offer,
        "iceServers": ice_servers,
    })

@app.route("/send_sdp_answer", methods=["POST"])
def send_sdp_answer():
    stream_id = request.json.get("streamId")
    answer = request.json.get("answer")

    headers = {
        "Authorization": f"Bearer {DID_API_KEY}",
        "Content-Type": "application/json"
    }

    requests.post(
        f"https://api.d-id.com/streams/{stream_id}/sdp",
        headers=headers,
        json={"answer": answer}
    )

    return jsonify({"status": "ok"})

@app.route("/send_ice_candidate", methods=["POST"])
def send_ice_candidate():
    stream_id = request.json.get("streamId")
    candidate = request.json.get("candidate")

    headers = {
        "Authorization": f"Bearer {DID_API_KEY}",
        "Content-Type": "application/json"
    }

    requests.post(
        f"https://api.d-id.com/streams/{stream_id}/ice",
        headers=headers,
        json={"candidate": candidate}
    )

    return jsonify({"status": "ok"})
