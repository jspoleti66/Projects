from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

DID_API_KEY = "tu_api_key_aqui"  # Cambia esto por tu clave real

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
