from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

DID_API_KEY = "Z29vZ2xlLW9hdXRoMnwxMDMzOTczMTI3MzI5NjkwMzI4Mjg6VElDajc1V0tZRGZXNzlLekxDOXAz"
DID_IMAGE_URL = "https://create-images-results.d-id.com/google-oauth2%7C103397312732969032828/64cc8a88-c3c3-4c71-9cb6-0e9b2641fa9c.png"  # imagen subida a D-ID

@app.route("/talk", methods=["POST"])
def talk():
    user_input = request.json.get("text", "")
    
    payload = {
        "script": {
            "type": "text",
            "input": user_input,
            "provider": {
                "type": "google",
                "voice_id": "es-US-Neural2-A"
            }
        },
        "source_url": DID_IMAGE_URL,
        "config": {
            "fluent": True,
            "pad_audio": 0.2
        }
    }

    headers = {
        "Authorization": f"Bearer {DID_API_KEY}",
        "Content-Type": "application/json"
    }

    # Enviar texto a D-ID
    response = requests.post("https://api.d-id.com/talks", headers=headers, json=payload)

    if response.status_code != 200:
        return jsonify({"error": "Error creando el video"}), 500

    video_url = response.json()["id"]

    # Esperar hasta que el video esté listo
    for _ in range(10):
        poll = requests.get(f"https://api.d-id.com/talks/{video_url}", headers=headers)
        data = poll.json()
        if data.get("result_url"):
            return jsonify({"video_url": data["result_url"]})
        time.sleep(2)

    return jsonify({"error": "El video no se generó a tiempo"}), 504

@app.route("/")
def home():
    return "Clon con D-ID activo"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
