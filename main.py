from flask import Flask, jsonify, request, render_template
import requests
import os

app = Flask(__name__)

DID_API_KEY = os.getenv("DID_API_KEY")
IMAGE_URL = "https://cdn.midjourney.com/85df418b-5cc6-47c8-80a3-729e2c6aeb27/0_2.png"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/init", methods=["POST"])
def init_stream():
    url = "https://api.d-id.com/talks/streams"
    headers = {
        "Authorization": f"Basic {DID_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "source_url": IMAGE_URL,
    }
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    return jsonify({
        "streamId": data.get("id"),
        "token": data.get("token")
    })

@app.route("/api/start", methods=["POST"])
def start_stream():
    content = request.json
    stream_id = content.get("streamId")
    text = content.get("text")

    url = f"https://api.d-id.com/talks/streams/{stream_id}"
    headers = {
        "Authorization": f"Basic {DID_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "script": {
            "type": "text",
            "input": text,
            "provider": {
                "type": "microsoft",
                "voice_id": "es-AR-ElenaNeural"
            }
        }
    }

    requests.post(url, json=payload, headers=headers)
    return jsonify({"status": "started"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
