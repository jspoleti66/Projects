# main.py

from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Cargar contexto desde archivos
BASE_PATH = "data"
ARCHIVOS = {
    "configuracion": ["prompt_sistema.txt", "instrucciones_generales.txt"],
    "conocimientos": ["cv.txt", "documentos_tecnicos.txt", "respuestas_frecuentes.txt"],
    "datos_personales": ["historia_personal.txt", "intereses.txt", "personalidad.txt"],
    "fuentes_conversacionales": ["chats.txt", "emails.txt"],
    "proyectos": ["proyectos_actuales.txt", "proyectos/tecnologias_utilizadas.txt"]
}

def cargar_contexto():
    contexto = ""
    for carpeta, archivos in ARCHIVOS.items():
        for archivo in archivos:
            ruta = os.path.join(BASE_PATH, carpeta, archivo)
            if os.path.exists(ruta):
                with open(ruta, "r", encoding="utf-8") as f:
                    contexto += f"\n### {archivo} ({carpeta})\n" + f.read() + "\n"
    return contexto.strip()

contexto_sistema = {
    "role": "system",
    "content": f"Eres un clon digital altamente personalizado. Solo responde con base en este contexto:\n{cargar_contexto()}"
}

# Consulta OpenRouter
def consultar_openrouter(historial):
    api_key = os.getenv("OPENROUTER_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://almostme-demo",
        "X-Title": "almostme-clon"
    }
    payload = {
        "model": "meta-llama/llama-4-maverick:free",
        "messages": historial,
        "temperature": 0.7
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    data = response.json()
    return data["choices"][0]["message"]["content"]


# Ruta API principal
@app.route("/clon", methods=["POST"])
def clon_endpoint():
    data = request.get_json()
    entrada_usuario = data.get("mensaje", "").strip()

    historial = [contexto_sistema, {"role": "user", "content": entrada_usuario}]
    respuesta = consultar_openrouter(historial)

