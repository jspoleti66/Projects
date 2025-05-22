from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='templates')
CORS(app)

HISTORY = []

# Cargar archivos de contexto (opcional)
CONTEXT = ""
for filename in os.listdir("data"):
    with open(os.path.join("data", filename), "r", encoding="utf-8") as f:
        CONTEXT += f.read() + "\n"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    HISTORY.append({"role": "user", "content": user_input})

    messages = [{"role": "system", "content": CONTEXT}] + HISTORY[-10:]

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json",
        },
        json={
            "model": "meta-llama/llama-4-maverick:free",
            "messages": messages,
        },
    )

    response_json = response.json()
    reply = response_json["choices"][0]["message"]["content"]
    HISTORY.append({"role": "assistant", "content": reply})
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
