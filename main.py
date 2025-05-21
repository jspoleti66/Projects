import requests
import base64
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DID_API_KEY = "WTJWallYSnlhWHB2WjBCbmJXRnBiQzVqYjIwOml6bTZaaEIzd29rQy1xUHBaVFlXSg=="
DID_BASE_URL = "https://api.d-id.com"

encoded_api_key = base64.b64encode(DID_API_KEY.encode("ascii")).decode("ascii")

HEADERS = {
    "Authorization": f"Basic {encoded_api_key}",
    "Content-Type": "application/json"
}

@app.route("/")
def index():
    return send_file("index.html")  # o usa templates + render_template

@app.route("/create_stream", methods=["POST"])
def create_stream():
    data = request.json
    source_url = data.get("source_url", "https://i.imgur.com/p0MUxcq.png")

    response = requests.post(
        f"{DID_BASE_URL}/talks/streams",
        headers=HEADERS,
        json={"source_url": source_url}
    )

    return jsonify(response.json()), response.status_code

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    prompt = data.get("message", "")
    return jsonify({"response": f"Recibí: {prompt}"})
