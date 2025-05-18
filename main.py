import os
import requests
import time
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DID_API_KEY = "Z29vZ2xlLW9hdXRoMnwxMDMzOTczMTI3MzI5NjkwMzI4Mjg6VElDajc1V0tZRGZXNzlLekxDOXAz"
DID_URL = "https://api.d-id.com/talks"

# Ruta principal
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# Cargar contexto
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

import os

DID_API_KEY = os.getenv("DID_API_KEY")

def generar_video_did(texto, avatar_url=None):
    headers = {
    "Authorization": f"Bearer {DID_API_KEY}",
    "Content-Type": "application/json"
}


def generar_video_did(texto, avatar_url=None):
    headers = {
    "Authorization": f"Bearer {"Y2VjYXJyaXpvZ0BnbWFpbC5jb20:KRphQ-Ulqibq5EpN8xj3f}",
    "Content-Type": "application/json"
    }

    payload = {
        "script": {
            "type": "text",
            "input": texto,
            "provider": {
                "type": "microsoft",
                "voice_id": "es-ES-AlvaroNeural"  # voz en español natural
            }
        },
        "source_url": avatar_url or "https://create-images-results.d-id.com/DefaultPresentationFace_v2.png"
    }

    response = requests.post(DID_URL, headers=headers, json=payload)
    if response.status_code != 200:
        return None, f"Error creando video: {response.text}"

    video_id = response.json()["id"]

    # Esperar a que esté listo
    for _ in range(10):
        time.sleep(2)
        status_response = requests.get(f"{DID_URL}/{video_id}", headers=headers)
        if status_response.status_code == 200:
            result = status_response.json()
            if result.get("result_url"):
                return result["result_url"], None

    return None, "⏱ Timeout esperando video"

@app.route("/clon", methods=["POST"])
def responder():
    datos = request.json
    entrada = datos.get("mensaje", "")
    mensajes = construir_mensaje_usuario(entrada, contexto)
    respuesta = consultar_openrouter(mensajes)

    video_url, error = generar_video_did(respuesta)

    if error:
        return jsonify({"error": error, "respuesta": respuesta})

    return jsonify({"respuesta": respuesta, "video_url": video_url})
