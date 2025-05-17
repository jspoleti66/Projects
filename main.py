import os
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Cargar contexto como en tu clon
def cargar_contexto():
    BASE_PATH = "data"
    ARCHIVOS = {
        "configuracion": ["prompt_sistema.txt", "instrucciones_generales.txt"],
        "conocimientos": ["cv.txt", "documentos_tecnicos.txt", "respuestas_frecuentes.txt"],
        "datos_personales": ["historia_personal.txt", "intereses.txt", "personalidad.txt"],
        "fuentes_conversacionales": ["chats.txt", "emails.txt"],
        "proyectos": ["proyectos_actuales.txt", "proyectos/tecnologias_utilizadas.txt"]
    }
    contexto = ""
    for carpeta, archivos in ARCHIVOS.items():
        for archivo in archivos:
            ruta = os.path.join(BASE_PATH, carpeta, archivo)
            if os.path.exists(ruta):
                with open(ruta, "r", encoding="utf-8") as f:
                    contexto += f"\n### Contenido de {archivo} (sección {carpeta})\n" + f.read() + "\n"
    return contexto

contexto = cargar_contexto()

def construir_mensaje_usuario(input_usuario, contexto):
    return [
        {
            "role": "system",
            "content": f"Eres un clon digital altamente personalizado. Responde únicamente en base al siguiente contexto: {contexto}. Si una pregunta no está relacionada, responde educadamente que no tienes información suficiente."
        },
        {
            "role": "user",
            "content": input_usuario
        }
    ]

def consultar_openrouter(mensajes):
    api_key = "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"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://almostme-demo",
        "X-Title": "almostme-clon"
    }
    payload = {
        "model": "meta-llama/llama-4-maverick:free",
        "messages": mensajes
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    if response.status_code != 200:
        return f"⚠️ Error: {response.text}"
    return response.json()["choices"][0]["message"]["content"]

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/clon", methods=["POST"])
def responder():
    datos = request.json
    entrada = datos.get("mensaje", "")
    mensajes = construir_mensaje_usuario(entrada, contexto)
    respuesta = consultar_openrouter(mensajes)
    return jsonify({"respuesta": respuesta})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
