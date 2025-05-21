from flask import Flask, request, jsonify, render_template
import requests
import base64

app = Flask(__name__)

# Tu API key en base64 para Authorization
API_KEY = "WTJWallYSnlhWHB2WjBCbmJXRnBiQzVqYjIwOml6bTZaaEIzd29rQy1xUHBaVFlXSg=="

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start-stream", methods=["POST"])
def start_stream():
    data = {
        "source_url": "https://raw.githubusercontent.com/jspoleti66/Projects/main/static/AlmostMe.png",
        "driver_url": "bank://lively"
    }
    
    headers = {
        "Authorization": f"Basic {API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.post("https://api.d-id.com/talks/streams", json=data, headers=headers)
    
    if response.ok:
        return jsonify(response.json())
    else:
        return jsonify({"error": response.text}), response.status_code

if __name__ == "__main__":
    app.run(debug=True)
