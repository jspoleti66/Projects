from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import subprocess
import uuid
import asyncio
import edge_tts
import time
import threading
import shutil

app = Flask(__name__)
FRAME_OUTPUT_DIR = "live_frames"
AUDIO_CACHE_DIR = "sadtalker/examples/driven_audio"
IMAGE_PATH = "sadtalker/examples/source_image/full_body_1.png"

# Crear directorios si no existen (FIX FileNotFoundError)
os.makedirs(FRAME_OUTPUT_DIR, exist_ok=True)
os.makedirs(AUDIO_CACHE_DIR, exist_ok=True)

# Limpieza periódica para sesiones viejas (>5 min)
def clean_old_sessions():
    while True:
        now = time.time()
        for folder in os.listdir(FRAME_OUTPUT_DIR):
            path = os.path.join(FRAME_OUTPUT_DIR, folder)
            if os.path.isdir(path):
                created = os.path.getctime(path)
                if now - created > 300:
                    shutil.rmtree(path, ignore_errors=True)
        for wav in os.listdir(AUDIO_CACHE_DIR):
            if wav.endswith(".wav"):
                wav_path = os.path.join(AUDIO_CACHE_DIR, wav)
                created = os.path.getctime(wav_path)
                if now - created > 300:
                    os.remove(wav_path)
        time.sleep(60)

threading.Thread(target=clean_old_sessions, daemon=True).start()

# Generar audio desde texto (para SadTalker, no se reproduce)
async def text_to_speech(text, wav_path):
    communicate = edge_tts.Communicate(text, voice="es-ES-ElviraNeural")
    await communicate.save(wav_path)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/animate", methods=["POST"])
def animate():
    text = request.json.get("text", "Hola, soy tu clon")
    session_id = str(uuid.uuid4())[:8]
    output_dir = os.path.join(FRAME_OUTPUT_DIR, session_id)
    os.makedirs(output_dir, exist_ok=True)

    driven_audio_path = os.path.join(AUDIO_CACHE_DIR, f"{session_id}.wav")
    asyncio.run(text_to_speech(text, driven_audio_path))

    command = [
        "python", "inference.py",
        "--driven_audio", driven_audio_path,
        "--source_image", IMAGE_PATH,
        "--result_dir", output_dir,
        "--enhancer", "gfpgan",
        "--preprocess", "full",
        "--still",
        "--batch_size", "1",
        "--pose_style", "0"
    ]

    try:
        print("▶ Ejecutando comando:", " ".join(command))
        subprocess.run(command, cwd="sadtalker", check=True, capture_output=True, text=True)
        first_frame = f"/live_frames/{session_id}/0.jpg"
        return jsonify({"status": "ok", "session": session_id, "frame": first_frame})
    except subprocess.CalledProcessError as e:
        print("❌ Error al ejecutar SadTalker:", e.stderr)
        return jsonify({"status": "error", "details": e.stderr or str(e)})

@app.route("/live_frames/<session>/<filename>")
def serve_frame(session, filename):
    return send_from_directory(os.path.join(FRAME_OUTPUT_DIR, session), filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
