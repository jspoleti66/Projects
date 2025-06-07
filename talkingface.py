import cv2
import numpy as np
import mediapipe as mp
import moviepy.editor as mpy

def generate_animation_from_text(image_path, text, output_path):
    # Carga imagen base
    img = cv2.imread(image_path)
    h, w, _ = img.shape

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)

    # Detectar landmarks faciales
    results = face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    if not results.multi_face_landmarks:
        raise Exception("No se detectaron rostros en la imagen")

    # Animación simple: genera cuadros modificando la boca y cabeza
    frames = []
    for i in range(15):
        frame = img.copy()

        # Simula movimiento de cabeza (rotación leve)
        angle = np.sin(i / 2) * 2
        M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1)
        frame = cv2.warpAffine(frame, M, (w, h))

        # Simula apertura de boca
        cv2.ellipse(frame, (w//2, int(h*0.65)), (20, 10 + i % 5), 0, 0, 360, (0, 0, 0), -1)

        frames.append(frame)

    # Guardar como video
    clip = mpy.ImageSequenceClip([cv2.cvtColor(f, cv2.COLOR_BGR2RGB) for f in frames], fps=10)
    clip.write_videofile(output_path, codec="libx264")
