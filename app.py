from flask import Flask, render_template, request, jsonify, send_from_directory
import os, subprocess, uuid, asyncio, hashlib, threading, time
import edge_tts

app = Flask(__name__)
FRAME_OUTPUT_DIR = "live_frames"
AUDIO_CACHE_DIR = "sadtalker/examples/driven_audio"
SOURCE_IMAGE = "sadtalker/examples/source_image/full_body_1.png"

# Limpia sesiones viejas automáticamente
def clean_old_sessions(max_age_sec=600):
    while True:
        now = time.time()
        for folder in os.listdir(FRAME_OUTPUT_DIR):
            path = os.path.join(FRAME_OUTPUT_DIR, folder)
            if os.path.isdir(path):
                age = now - os.path.getmtime(path)
                if age > max_age_sec:
                    try:
                        for f in os.listdir(path):
                            os.remove(os.path.join(path, f))
                        os.rmdir(path)
                        print(f"🧹 Sesión vieja eliminada: {folder}")
                    except Exception as e:
                        print(f"Error al borrar sesión {folder}: {e}")
        time.sleep(300)

# Inicia limpieza automática en segundo plano
threading.Thread(target=clean_old_sessions, daemon=True).start()

async def generate_tts(text, path):
    communicate = edge_tts.Communicate(text, voice="es-ES-ElviraNeural")
    await communicate.save(path)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/animate", methods=["POST"])
def animate():
    text = request.json.get("text", "").strip()
    if not text:
        return jsonify({"status": "error", "details": "Texto vacío"})

    session_id = str(uuid.uuid4())[:8]
    output_dir = os.path.join(FRAME_OUTPUT_DIR, session_id)
    os.makedirs(output_dir, exist_ok=True)

    # Usa hash MD5 del texto para cachear TTS
    text_hash = hashlib.md5(text.encode()).hexdigest()
    audio_path = os.path.join(AUDIO_CACHE_DIR, f"{text_hash}.wav")

    try:
        if not os.path.exists(audio_path):
            asyncio.run(generate_tts(text, audio_path))

        command = [
            "python", "inference.py",
            "--driven_audio", audio_path,
            "--source_image", SOURCE_IMAGE,
            "--result_dir", output_dir,
            "--enhancer", "gfpgan",
            "--preprocess", "full",
            "--still",
            "--batch_size", "1",
            "--pose_style", "0"
        ]

        subprocess.run(command, cwd="sadtalker", check=True, capture_output=True, text=True)
        return jsonify({"status": "ok", "session": session_id})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "details": e.stderr.strip()})
    except Exception as e:
        return jsonify({"status": "error", "details": str(e)})

@app.route("/live_frames/<session>/<filename>")
def serve_frame(session, filename):
    return send_from_directory(os.path.join(FRAME_OUTPUT_DIR, session), filename)

if __name__ == "__main__":
    os.makedirs(FRAME_OUTPUT_DIR, exist_ok=True)
    os.makedirs(AUDIO_CACHE_DIR, exist_ok=True)
    app.run(host="0.0.0.0", port=10000)
