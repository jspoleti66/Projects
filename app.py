from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import subprocess
import uuid
import asyncio
import edge_tts  # Asegurate de instalarlo: pip install edge-tts

app = Flask(__name__)
FRAME_OUTPUT_DIR = "live_frames"
IMAGE_PATH = "sadtalker/examples/source_image/full_body_1.png"

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

    driven_audio_path = f"sadtalker/examples/driven_audio/{session_id}.wav"
    asyncio.run(text_to_speech(text, driven_audio_path))  # genera WAV solo para SadTalker

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
        print("Ejecutando comando:", " ".join(command))
        subprocess.run(command, cwd="sadtalker", check=True, capture_output=True, text=True)
        first_frame = f"/live_frames/{session_id}/0.jpg"
        return jsonify({"status": "ok", "session": session_id, "frame": first_frame})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "details": e.stderr or str(e)})

@app.route('/live_frames/<session>/<filename>')
def serve_frame(session, filename):
    return send_from_directory(os.path.join(FRAME_OUTPUT_DIR, session), filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
