from flask import Flask, request, render_template
import cv2
import os

app = Flask(__name__)

# Asegurar que el directorio 'static/' exista
os.makedirs("static", exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form.get("text", "").lower()

        # Cargar la imagen base
        img = cv2.imread("static/AlmostMe.png")
        if img is None:
            return "Error: No se encontró la imagen base."

        # Simular boca abierta si hay vocales
        if any(v in text for v in "aeiou"):
            height, width = img.shape[:2]
            center_x = width // 2
            center_y = int(height * 0.65)

            # Dibujar una elipse negra como boca abierta
            cv2.ellipse(img, (center_x, center_y), (30, 15), 0, 0, 360, (0, 0, 0), -1)

        # Guardar imagen generada
        output_path = "static/generated.png"
        cv2.imwrite(output_path, img)

    return render_template("index.html")
