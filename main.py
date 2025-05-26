from flask import Flask, send_from_directory, jsonify, request
import requests
import os

app = Flask(__name__, static_folder="static", static_url_path="/static")

DID_API_KEY = os.environ.get("DID_API_KEY")
IMAGE_URL = "https://raw.githubusercontent.com/jspoleti66/Projects/main/static/AlmostMe.png"

@app.route("/")
def serve_index():
    return send_from_directory(".", "index.html")  # Sirve el index.html en raíz

@app.route("/api/init", methods=["POST"])
def init_stream():
    url = "https://api.d-id.com/talks/streams"
    headers = {
        "Authorization": f"Basic {DID_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"source_url": IMAGE_URL}
    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        print("API Response:", data)

        return jsonify({
            "streamId": data.get("id"),
            "token": data.get("session_id")  # <- corregido aquí
        })

        return jsonify({
            "streamId": data.get("id"),
            "token": data.get("session_id")  # <- corregido aquí
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Failed to init stream"}), 500

if __name__ == "__main__":
    app.run(debug=True)
