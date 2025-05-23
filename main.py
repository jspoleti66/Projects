from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')

DID_API_KEY = os.environ.get("DID_API_KEY")

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/create_stream", methods=["POST"])
def create_stream():
    if not DID_API_KEY:
        return jsonify({"error": "Falta la clave DID_API_KEY en el entorno"}), 500

    user_text = request.json.get("text", "Hola, soy tu clon AlmostMe")

    headers = {
        "Authorization": f"Basic {DID_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "source_url": "https://raw.githubusercontent.com/jspoleti66/Projects/main/static/AlmostMe.png",
        "script": {
            "type": "text",
            "input": user_text,
            "provider": {
                "type": "microsoft",
                "voice_id": "es-ES-AlvaroNeural"
            }
        },
        "config": {
            "stitch": True,
            "driver_expressions": {
                "expressions": [
                    {"expression": "happy", "start_frame": 0, "intensity": 0.4}
                ]
            }
        }
    }

    try:
        response = requests.post(
            "https://api.d-id.com/talks/streams",
            headers=headers,
            json=body
        )
        response.raise_for_status()
        data = response.json()

        return jsonify({
            "streamId": data.get("id"),
            "sdp": data.get("offer"),
            "iceServers": data.get("ice_servers", [])
        })

    except requests.RequestException as e:
        print("❌ Error al contactar la API de D-ID:", e)
        return jsonify({"error": "Error al contactar la API de D-ID", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
