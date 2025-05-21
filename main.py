from flask import Flask, request, jsonify
import requests
import base64

app = Flask(__name__)

# Puedes ocultar esta clave en variables de entorno en producción
D_ID_AUTH_HEADER = "WTJWallYSnlhWHB2WjBCbmJXRnBiQzVqYjIwOml6bTZaaEIzd29rQy1xUHBaVFlXSg=="
API_URL = "https://api.d-id.com/talks/streams"

@app.route('/start-stream', methods=['POST'])
def start_stream():
    # Puedes extender esto para recibir `source_url` y `driver_url` como parámetros
    payload = {
        "source_url": "https://raw.githubusercontent.com/jspoleti66/Projects/main/static/AlmostMe.png",
        "driver_url": "bank://lively"
    }

    headers = {
        "Authorization": f"Basic {D_ID_AUTH_HEADER}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return 'D-ID Stream Web Service Ready 🚀'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
