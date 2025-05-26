import os
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

DID_TOKEN = os.getenv("DID_TOKEN")  # Obligatorio, debe estar en variables de entorno en Render

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route("/d-id-stream", methods=["POST"])
def d_id_stream():
    data = request.json
    texto = data.get("texto", "Hola desde AlmostMe con D-ID!")

    headers = {
        "Authorization": f"Bearer {DID_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "script": {
            "type": "text",
            "input": texto,
            "provider": {"type": "microsoft", "voice_id": "es-ES-ElviraNeural"}
        },
        "config": {"fluent": True, "pad_audio": 0.5},
        "image_url": "https://i.imgur.com/p0MUxcq.png"
    }

    resp = requests.post("https://api.d-id.com/talks/streams", headers=headers, json=payload)

    if resp.status_code == 200:
        return jsonify(resp.json())
    else:
        return jsonify({"error": resp.text}), resp.status_code


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
