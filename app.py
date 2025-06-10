from flask import Flask, request, jsonify, render_template
import subprocess
import os
import uuid

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/animate', methods=['POST'])
def animate():
    data = request.get_json()
    text = data.get("text", "Hola, esta es una demo")

    # Ruta a SadTalker
    SADTALKER_DIR = "sadtalker"
    AUDIO_PATH = os.path.join(SADTALKER_DIR, "examples", "driven_audio", "sample.wav")
    IMAGE_PATH = os.path.join(SADTALKER_DIR, "examples", "source_image", "full_body_1.png")

    # Ruta de salida única
    output_id = str(uuid.uuid4())[:8]
    output_dir = os.path.join("live_frames", output_id)
    os.makedirs(output_dir, exist_ok=True)

    # Comando para ejecutar inference.py
    cmd = [
        "python", "inference.py",
        "--driven_audio", AUDIO_PATH,
        "--source_image", IMAGE_PATH,
        "--result_dir", f"../{output_dir}",
        "--enhancer", "gfpgan",
        "--preprocess", "full",
        "--still",
        "--batch_size", "1",
        "--pose_style", "0"
    ]

    try:
        result = subprocess.run(
            cmd,
            cwd=SADTALKER_DIR,
            check=True,
            capture_output=True,
            text=True
        )
        return jsonify({
            "status": "success",
            "folder": output_dir
        })
    except subprocess.CalledProcessError as e:
        return jsonify({
            "status": "error",
            "details": e.stderr or str(e)
        })

if __name__ == '__main__':
    app.run(debug=True, port=10000)
