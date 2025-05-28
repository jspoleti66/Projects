from flask import Flask, render_template, request, jsonify
import requests
import os
import base64

app = Flask(__name__, static_folder="static", static_url_path="/static", template_folder="templates")

# Define tus credenciales explícitamente o usa variables de entorno
email = os.getenv("DID_EMAIL") or "cecarrizog@gmail.com"
api_key = os.getenv("DID_API_KEY") or "Y2VjYXJyaXpvZ0BnbWFpbC5jb20:AJQHqsCbFTHgXkfVfP8zd"
AVATAR_URL = "https://raw.githubusercontent.com/jspoleti66/Projects/main/static/AlmostMe.png"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start-stream", methods=["POST"])
def start_stream():
    headers_start = {
        'Authorization': 'Basic ' + base64.b64encode(f'{email}:{api_key}'.encode()).decode(),
        'Content-Type': 'application/json'
    }

    payload = {
        "source_url": AVATAR_URL,
        "config": {"fluent": True}
    }

    print("🟡 Enviando solicitud a D-ID (start-stream)")
    print("🔹 Headers:", headers_start)
    print("🔹 Payload:", payload)

    response = requests.post("https://api.d-id.com/talks/streams", headers=headers_start, json=payload)
    print("🟢 Respuesta de D-ID (start-stream):", response.status_code, response.text)

    return jsonify(response.json()), response.status_code

@app.route("/send-offer", methods=["POST"])
def send_offer():
    data = request.get_json()
    stream_id = data.get("stream_id")
    offer_sdp = data.get("offer")

    headers_offer = {
        'Authorization': 'Basic ' + base64.b64encode(f'{email}:{api_key}'.encode()).decode(),
        'Content-Type': 'application/json'
    }

    payload = {
        "sdp": offer_sdp
    }

    url = f"https://api.d-id.com/streams/{stream_id}/sdp"

    print("🟡 Enviando oferta SDP")
    print("🔹 Stream ID:", stream_id)
    print("🔹 Headers:", headers_offer)
    print("🔹 Payload:", payload)

    response = requests.post(url, headers=headers_offer, json=payload)
    print("🟢 Respuesta de D-ID (send-offer):", response.status_code, response.text)

    return jsonify(response.json()), response.status_code

if __name__ == "__main__":
    print("🚀 Servidor iniciado en modo debug")
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
