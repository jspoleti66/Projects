
from flask import Flask, request, render_template, jsonify
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form.get("text", "")
        print(f"Texto recibido: {text}")
        # Aquí se debería hacer la conversión TTS y animación (mockeado por ahora)
        return jsonify({ "status": "ok", "message": f"Texto procesado: {text}" })
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
