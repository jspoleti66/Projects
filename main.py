from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')

# Leer la clave D-ID desde variable de entorno
DID_API_KEY = os.environ.get("DID_API_KEY")

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Crear el stream y devolver SDP + ICE servers
@app.route("/create_stream", methods=["POST"])
def create_stream():
    if not DID_API_KEY:
        return jsonify({"error": "Falta la clave DID_API_KEY"}), 500

    sdp_offer = request.json.get("sdpOffer")
    if not sdp_offer:
        return jsonify({"error": "Falta sdpOffer"}), 400

    headers = {
        "Authorization": f"Basic {DID_API_KEY}",  # Usamos Basic Auth si ya está en base64
        "Content-Type": "application/json"
    }

    body = {
        "source_url": "https://raw.githubusercontent.com/jspoleti66/Projects/main/static/AlmostMe.png",
        "config": {
            "stitch": True,
            "driver_expressions": {
                "expressions": [
                    {"expression": "neutral", "start_frame": 0, "intensity": 0.5}
                ]
            }
        },
        "offer": sdp_offer,
        "script": {
            "type": "text",
            "input": "Hola, soy tu clon AlmostMe",
            "provider": {
                "type": "microsoft",
                "voice_id": "es-ES-AlvaroNeural"
            },
            "ssml": False
        }
    }

    try:
        response = requests.post("https://api.d-id.com/talks/streams", headers=headers, json=body)
        response.raise_for_status()
        data = response.json()

        return jsonify({
            "streamId": data.get("id"),
            "sdp": data.get("answer"),
            "iceServers": data.get("ice_servers", [])
        })
    except requests.RequestException as e:
        print(f"Error al contactar la API de D-ID: {e}")
        return jsonify({"error": "Error al contactar la API de D-ID", "details": str(e)}), 500

# Recibir ICE candidates desde el frontend y enviarlos a D-ID
@app.route("/send_ice_candidate", methods=["POST"])
def send_ice_candidate():
    if not DID_API_KEY:
        return jsonify({"error": "Falta la clave DID_API_KEY"}), 500

    data = request.json
    stream_id = data.get("streamId")
    candidate = data.get("candidate")

    if not stream_id or not candidate:
        return jsonify({"error": "Faltan datos"}), 400

    headers = {
        "Authorization": f"Basic {DID_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            f"https://api.d-id.com/talks/streams/{stream_id}/ice",
            headers=headers,
            json={"candidate": candidate}
        )
        response.raise_for_status()
        return jsonify({"success": True})
    except requests.RequestException as e:
        print(f"Error al enviar ICE candidate: {e}")
        return jsonify({"error": "Error al enviar ICE candidate", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
