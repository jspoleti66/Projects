from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__, static_url_path='', static_folder='static')

DID_API_KEY = "WTJWallYSnlhWHB2WjBCbmJXRnBiQzVqYjIwOml6bTZaaEIzd29rQy1xUHBaVFlXSg=="  # Cambia esto por tu clave real

# Servir index.html en la raíz /
@app.route("/")
def index():
    return app.send_static_file("index.html")

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
            }
        },
        "script": {
            "type": "text",
            "input": user_text,
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

        print("D-ID API Response:", data)

        stream_id = data.get("id")
        sdp_offer = data.get("offer")
        ice_servers = data.get("ice_servers", [])

        if not sdp_offer:
            return jsonify({"error": "No SDP offer from D-ID API", "details": data}), 500

        return jsonify({
            "streamId": stream_id,
            "sdp": sdp_offer,
            "iceServers": ice_servers
        })

    except requests.RequestException as e:
        print(f"Error calling D-ID API: {e}")
        return jsonify({"error": "Failed to contact D-ID API", "details": str(e)}), 500

# Aquí se deben implementar los endpoints para manejar ICE candidates y SDP answer
@app.route("/send_ice_candidate", methods=["POST"])
def send_ice_candidate():
    data = request.json
    # Aquí deberías enviar el candidate al servidor D-ID para ese streamId
    # Como no hay API pública documentada, solo respondemos OK por ahora
    print("Received ICE candidate:", data)
    return jsonify({"status": "candidate received"}), 200

@app.route("/send_sdp_answer", methods=["POST"])
def send_sdp_answer():
    data = request.json
    # Aquí deberías enviar el SDP answer al servidor D-ID para ese streamId
    print("Received SDP answer:", data)
    return jsonify({"status": "sdp answer received"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
