from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

D_ID_AUTH_HEADER = "Basic WTJWallYSnlhWHB2WjBCbmJXRnBiQzVqYjIwOml6bTZaaEIzd29rQy1xUHBaVFlXSg=="
API_URL = "https://api.d-id.com/talks/streams"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start-stream', methods=['POST'])
def start_stream():
    payload = {
        "source_url": "https://raw.githubusercontent.com/jspoleti66/Projects/main/static/AlmostMe.png",
        "driver_url": "bank://lively",
        "script": {
            "type": "text",
            "input": "Hola, soy tu clon parlante generado en tiempo real con D-ID."
        }
    }

    headers = {
        "Authorization": D_ID_AUTH_HEADER,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.after_request
def add_headers(response):
    response.headers['X-Frame-Options'] = 'ALLOWALL'
    response.headers['Content-Security-Policy'] = "default-src * 'unsafe-inline' 'unsafe-eval'; script-src * 'unsafe-inline' 'unsafe-eval'; connect-src *; frame-src *; img-src * data:; style-src * 'unsafe-inline';"
    return response
