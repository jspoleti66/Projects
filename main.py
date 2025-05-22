from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Reemplaza con tu clave de API de D-ID
D_ID_API_KEY = "Y2VjYXJyaXpvZ0BnbWFpbC5jb20:T8blqywKs5-5ky13iUJtg"
API_URL = "https://api.d-id.com/talks"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start-talk', methods=['POST'])
def start_talk():
    payload = {
        "source_url": "https://raw.githubusercontent.com/jspoleti66/Projects/main/static/AlmostMe.png",
        "script": {
            "type": "text",
            "input": "Hola, soy tu clon parlante generado con D-ID."
        }
    }

    headers = {
        "Authorization": f"Basic {D_ID_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        talk_id = data.get("id", "")
        return jsonify({"talk_id": talk_id})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-talk/<talk_id>', methods=['GET'])
def get_talk(talk_id):
    headers = {
        "Authorization": f"Basic {D_ID_API_KEY}",
        "Accept": "application/json"
    }

    try:
        response = requests.get(f"{API_URL}/{talk_id}", headers=headers)
        response.raise_for_status()
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.after_request
def add_headers(response):
    response.headers['X-Frame-Options'] = 'ALLOWALL'
    response.headers['Content-Security-Policy'] = (
        "default-src *; "
        "frame-src *; "
        "script-src * 'unsafe-inline'; "
        "style-src * 'unsafe-inline'; "
        "connect-src *; "
        "img-src *;"
    )
    return response

if __name__ == '__main__':
    app.run(debug=True)
