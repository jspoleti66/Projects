import os
import requests

# Ruta base donde están los archivos
BASE_PATH = "data"

# Archivos esperados organizados por carpeta
ARCHIVOS = {
    "configuracion": ["prompt_sistema.txt", "instrucciones_generales.txt"],
    "conocimientos": ["cv.txt", "documentos_tecnicos.txt", "respuestas_frecuentes.txt"],
    "datos_personales": ["historia_personal.txt", "intereses.txt", "personalidad.txt"],
    "fuentes_conversacionales": ["chats.txt", "emails.txt"],
    "proyectos": ["proyectos_actuales.txt", "proyectos/tecnologias_utilizadas.txt"]
}

# Leer todo el contenido de los archivos
def cargar_contexto():
    contexto = ""
    for carpeta, archivos in ARCHIVOS.items():
        for archivo in archivos:
            ruta = os.path.join(BASE_PATH, carpeta, archivo)
            if os.path.exists(ruta):
                with open(ruta, "r", encoding="utf-8") as f:
                    contexto += f"\n### Contenido de {archivo} (sección {carpeta})\n" + f.read() + "\n"
            else:
                print(f"⚠️ Archivo no encontrado: {ruta}")
    return contexto.strip()

# Enviar consulta a OpenRouter usando meta-llama/llama-4-maverick:free
def consultar_openrouter(mensajes):
    api_key = os.getenv("OPENROUTER_API_KEY") or "TU_API_KEY_AQUI"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://almostme-demo",
        "X-Title": "almostme-clon"
    }

    payload = {
        "model": "meta-llama/llama-4-maverick:free",
        "messages": mensajes,
        "temperature": 0.7
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

    try:
        data = response.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        elif "error" in data:
            return f"⚠️ Error del modelo: {data['error'].get('message', 'Respuesta inválida')}"
        else:
            return "⚠️ El modelo no devolvió una respuesta válida."
    except Exception as e:
        return f"⚠️ Error procesando la respuesta del modelo: {e}"

# Función principal interactiva con historial de conversación
def main():
    contexto = cargar_contexto()
    historial = [{
        "role": "system",
        "content": f"Eres un clon digital altamente personalizado. Responde únicamente en base al siguiente contexto: {contexto}. Si una pregunta no está relacionada, responde educadamente que no tienes información suficiente."
    }]

    print("🤖 Clon interactivo iniciado. Escribe tu mensaje (o 'salir' para terminar, 'reset' para reiniciar contexto).\n")

    while True:
        entrada = input("👤 Usuario: ").strip()
        if entrada.lower() in ["salir", "exit", "quit"]:
            break
        if entrada.lower() == "reset":
            historial = historial[:1]  # Mantener solo el mensaje de sistema
            print("🔄 Historial reiniciado.")
            continue

        historial.append({"role": "user", "content": entrada})
        try:
            respuesta = consultar_openrouter(historial)
            historial.append({"role": "assistant", "content": respuesta})
            print(f"🤖 Clon: {respuesta}\n")
        except Exception as e:
            print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    main()
