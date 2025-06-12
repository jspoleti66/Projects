from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import subprocess
import uuid

app = Flask(__name__)
FRAME_OUTPUT_DIR = "live_frames"
IMAGE_PATH = "sadtalker/examples/source_image/full_body_1.png"
DRIVEN_AUDIO_PATH = "sadtalker/examples/driven_audio/sample.wav"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/animate", methods=["POST"])
def animate():
    text = request.json.get("text", "Hola, soy tu clon")

    session_id = str(uuid.uuid4())[:8]
    output_dir = os.path.join(FRAME_OUTPUT_DIR, session_id)
    os.makedirs(output_dir, exist_ok=True)

    command = [
        "python", "inference.py",
        "--driven_audio", DRIVEN_AUDIO_PATH,
        "--source_image", IMAGE_PATH,
        "--result_dir", output_dir,
        "--enhancer", "gfpgan",
        "--preprocess", "full",  # ← valor corregido aquí
        "--still",
        "--batch_size", "1",
        "--pose_style", "0"
    ]

    try:
        print("Ejecutando comando:", " ".join(command))
        result = subprocess.run(
            command,
            cwd="sadtalker",
            check=True,
            capture_output=True,
            text=True
        )
        print("STDOUT:", result.stdout)
        return jsonify({"status": "ok", "session": session_id})
    except subprocess.CalledProcessError as e:
        print("ERROR:", e.stderr)
        return jsonify({
            "status": "error",
            "details": e.stderr or str(e)
        })

@app.route('/live_frames/<session>/<filename>')
def serve_frame(session, filename):
    return send_from_directory(os.path.join(FRAME_OUTPUT_DIR, session), filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
