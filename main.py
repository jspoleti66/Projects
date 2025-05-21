import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DID_API_KEY = "WTJWallYSnlhWHB2WjBCbmJXRnBiQzVqYjIwOml6bTZaaEIzd29rQy1xUHBaVFlXSg=="
DID_BASE_URL = "https://api.d-id.com"

HEADERS = {
    "Authorization": f"Basic {DID_API_KEY.encode('ascii').hex()}",
    "Content-Type": "application/json"
}

@app.route("/create_stream", methods=["POST"])
def create_stream():
    data = request.json
    source_url = data.get("source_url", "https://i.imgur.com/p0MUxcq.png")

    response = requests.post(
        f"{DID_BASE_URL}/talks/streams",
        headers={
            "Authorization": f"Basic {DID_API_KEY}:",
            "Content-Type": "application/json"
        },
        json={"source_url": source_url}
    )

    return jsonify(response.json()), response.status_code

