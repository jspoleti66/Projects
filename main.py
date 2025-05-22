from flask import Flask, request, jsonify, send_from_directory
import requests
import os
import time

app = Flask(__name__, static_url_path='/static')

DID_API_KEY = os.getenv("DID_API_KEY")  # Asegurate de setear esto en Render
DID_BASE_URL = "https://api.d-id.com/talks"

headers = {
    "Authorization": f"Basic {DID_API_KEY}",
    "Content-Type": "application/json"
}

# Imagen pública y texto demo
IMAGE_URL = "https://i.imgur.com/YOUR_IMAGE.jpg"  # Cambiar por tu imagen
DEFAULT_TEXT = "Hola, soy tu clon digital. ¿En qué puedo ayudarte?"

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/start-talk", methods=["POST"])
def start_talk():
    payload = {
        "source_url": IMAGE_URL,
        "script": {
            "type": "text",
            "input": DEFAULT_TEXT,
            "provider": {
                "type": "microsoft",
                "voice_id": "es-ES-AlvaroNeural"
            }
        }
    }

    response = requests.post(DID_BASE_URL, headers=headers, json=payload)

    if response.status_code == 201:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Error al iniciar el video", "details": response.text}), 500

@app.route("/check-status/<talk_id>")
def check_status(talk_id):
    status_url = f"{DID_BASE_URL}/{talk_id}"
    response = requests.get(status_url, headers=headers)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "No se pudo consultar el estado", "details": response.text}), 500

# Permitir favicon (opcional)
@app.route("/favicon.ico")
def favicon():
    return "", 204
