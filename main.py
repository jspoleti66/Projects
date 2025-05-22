from flask import Flask, request, jsonify, render_template
import requests
import os
import base64

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start-stream", methods=["POST"])
def start_stream():
    api_key = os.getenv("DID_API_KEY")
    if not api_key:
        return jsonify({"error": "DID_API_KEY no está configurada"}), 500

    auth_header = base64.b64encode(f"{api_key}:".encode()).decode()

    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/json"
    }

    payload = {
        "source_url": "https://i.imgur.com/yVX4S5G.png",  # Cambiá esta URL por tu imagen si querés
        "config": {
            "driver_expressions": {
                "expressions": ["neutral"]
            },
            "align_driver": True
        }
    }

    response = requests.post("https://api.d-id.com/talks/streams", json=payload, headers=headers)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": response.text}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
