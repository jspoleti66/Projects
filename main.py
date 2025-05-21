import requests
import base64
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# API Key en formato user:api_key, ya codificada en Base64
DID_API_KEY = "WTJWallYSnlhWHB2WjBCbmJXRnBiQzVqYjIwOml6bTZaaEIzd29rQy1xUHBaVFlXSg=="
DID_BASE_URL = "https://api.d-id.com"

HEADERS = {
    "Authorization": f"Basic {DID_API_KEY}",
    "Content-Type": "application/json"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_stream", methods=["POST"])
def create_stream():
    data = request.get_json()
    source_url = data.get("source_url", "https://raw.githubusercontent.com/jspoleti66/Projects/main/static/AlmostMe.png")

    # Crear stream
    response = requests.post(
        f"{DID_BASE_URL}/talks/streams",
        headers=HEADERS,
        json={"source_url": source_url}
    )

    if response.status_code != 200:
        return jsonify({"error": "Error al crear el stream", "details": response.json()}), response.status_code

    result = response.json()

    # Devolver solo lo necesario
    return jsonify({
        "id": result.get("id"),
        "session_id": result.get("session_id"),
        "offer": result.get("offer", {}).get("sdp"),
        "ice_servers": result.get("ice_servers", [])
    })

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    prompt = data.get("message", "")
    return jsonify({"response": f"Recibí: {prompt}"})
