from flask import Flask, request, jsonify, send_file, render_template
import requests
import os
import uuid
from TTS.api import TTS

app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
tts = TTS(model_name="tts_models/es/mai/tacotron2-DDC", progress_bar=False, gpu=False)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/clon", methods=["POST"])
def clon():
    data = request.json
    texto_entrada = data.get("mensaje", "")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta-llama/llama-4-maverick:free",
        "messages": [
            {"role": "system", "content": "Eres un clon digital que responde de forma clara."},
            {"role": "user", "content": texto_entrada}
        ]
    }
    resp = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    if resp.status_code != 200:
        return jsonify({"error": "Error en OpenRouter", "detalle": resp.text}), 500

    respuesta_texto = resp.json()["choices"][0]["message"]["content"]

    filename = f"static/audio_{uuid.uuid4().hex}.wav"
    if not os.path.exists("static"):
        os.makedirs("static")

    tts.tts_to_file(text=respuesta_texto, file_path=filename)

    return jsonify({
        "respuesta": respuesta_texto,
        "audio_url": "/" + filename
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
