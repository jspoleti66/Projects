from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Cambia este por tu API Key D-ID base64 "Basic xxx"
D_ID_AUTH_HEADER = "Basic WTJWallYSnlhWHB2WjBCbmJXRnBiQzVqYjIwOml6bTZaaEIzd29rQy1xUHBaVFlXSg=="

HEADERS = {
    "Authorization": D_ID_AUTH_HEADER,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

BASE_URL = "https://api.d-id.com"

# Variable global para guardar talkId (en producción usar DB o contexto)
talk_id_global = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start-talk", methods=["POST"])
def start_talk():
    global talk_id_global
    payload = {
        "source_url": "https://raw.githubusercontent.com/jspoleti66/Projects/main/static/AlmostMe.png",
        "driver_url": "bank://lively",
        "script": {
            "type": "text",
            "input": "Hola, soy tu clon parlante generado con D-ID."
        },
        "streaming": True
    }
    try:
        res = requests.post(f"{BASE_URL}/talks", json=payload, headers=HEADERS)
        res.raise_for_status()
        data = res.json()
        talk_id_global = data.get("id")
        return jsonify({"talk_id": talk_id_global})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/webrtc-offer/<talk_id>")
def webrtc_offer(talk_id):
    try:
        res = requests.get(f"{BASE_URL}/talks/{talk_id}/webrtc", headers=HEADERS)
        res.raise_for_status()
        data = res.json()
        return jsonify({"sdp": data.get("sdp")})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/webrtc-answer/<talk_id>", methods=["POST"])
def webrtc_answer(talk_id):
    sdp = request.json.get("sdp")
    if not sdp:
        return jsonify({"error": "No SDP provided"}), 400
    try:
        res = requests.post(f"{BASE_URL}/talks/{talk_id}/webrtc", json={"sdp": sdp}, headers=HEADERS)
        res.raise_for_status()
        return jsonify({"result": "Answer accepted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/webrtc-candidate/<talk_id>", methods=["POST"])
def webrtc_candidate(talk_id):
    candidate = request.json.get("candidate")
    if not candidate:
        return jsonify({"error": "No candidate provided"}), 400
    try:
        res = requests.post(f"{BASE_URL}/talks/{talk_id}/webrtc/candidates", json={"candidate": candidate}, headers=HEADERS)
        res.raise_for_status()
        return jsonify({"result": "Candidate accepted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
