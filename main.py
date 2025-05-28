from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__, static_folder="static", static_url_path="/static", template_folder="templates")

DID_API_KEY = os.getenv("DID_API_KEY")
AVATAR_URL = "https://raw.githubusercontent.com/jspoleti66/Projects/main/static/AlmostMe.png"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start-stream", methods=["POST"])
def start_stream():
    headers = {
        "Authorization": f"Bearer {DID_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "source_url": AVATAR_URL,
        "config": {"fluent": True}
    }

    print("🟡 Enviando solicitud a D-ID (start-stream)")
    print("🔹 Headers:", headers)
    print("🔹 Payload:", payload)

    response = requests.post("https://api.d-id.com/talks/streams", headers=headers, json=payload)
    print("🟢 Respuesta de D-ID (start-stream):", response.status_code, response.text)

    return jsonify(response.json())

@app.route("/send-offer", methods=["POST"])
def send_offer():
    data = request.get_json()
    stream_id = data["stream_id"]
    offer_sdp = data["offer"]

    headers = {
        "Authorization": f"Bearer {DID_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "sdp": offer_sdp
    }

    url = f"https://api.d-id.com/streams/{stream_id}/sdp"

    print("🟡 Enviando oferta SDP")
    print("🔹 Stream ID:", stream_id)
    print("🔹 Headers:", headers)
    print("🔹 Payload:", payload)

    response = requests.post(url, headers=headers, json=payload)
    print("🟢 Respuesta de D-ID (send-offer):", response.status_code, response.text)

    return jsonify(response.json())

if __name__ == "__main__":
    print("🚀 Servidor iniciado en modo debug")
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
