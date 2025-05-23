from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
DID_API_KEY = os.getenv("DID_API_KEY", "WTJWallYSnlhWHB2WjBCbmJXRnBiQzVqYjIwOml6bTZaaEIzd29rQy1xUHBaVFlXSg==")  # o usa una variable de entorno

@app.route("/create_stream", methods=["POST"])
def create_stream():
    sdp_offer = request.json.get("sdpOffer", {}).get("sdp")
    if not sdp_offer:
        return jsonify({"error": "SDP offer is required"}), 400

    headers = {
        "Authorization": f"Bearer {DID_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "offer": {
            "type": "offer",
            "sdp": sdp_offer
        },
        "avatar_url": "https://raw.githubusercontent.com/jspoleti66/Projects/main/static/AlmostMe.png",
        "config": {
            "stitch": True
        },
        "script": {
            "type": "text",
            "input": "Hola, soy tu clon interactivo AlmostMe",
            "provider": {
                "type": "microsoft",
                "voice_id": "es-ES-AlvaroNeural"
            }
        }
    }

    try:
        response = requests.post("https://api.d-id.com/talks/streams", headers=headers, json=body)
        response.raise_for_status()
        data = response.json()

        return jsonify({
            "streamId": data.get("id"),
            "sdpAnswer": data.get("answer"),
            "iceServers": data.get("ice_servers", [])
        })

    except requests.RequestException as e:
        print(f"Error al llamar D-ID: {e}")
        return jsonify({"error": "Fallo al contactar con D-ID", "details": str(e)}), 500

@app.route("/send_ice_candidate", methods=["POST"])
def send_ice_candidate():
    data = request.json
    stream_id = data.get("streamId")
    candidate = data.get("candidate")

    if not stream_id or not candidate:
        return jsonify({"error": "streamId y candidate son obligatorios"}), 400

    headers = {
        "Authorization": f"Bearer {DID_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            f"https://api.d-id.com/talks/streams/{stream_id}/ice",
            headers=headers,
            json={"candidate": candidate}
        )
        response.raise_for_status()
        return jsonify({"status": "ok"})
    except requests.RequestException as e:
        print(f"Error al enviar ICE: {e}")
        return jsonify({"error": "Fallo al enviar ICE", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
