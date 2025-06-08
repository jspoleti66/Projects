
import os
from PIL import Image, ImageDraw

def animate_from_text(text):
    base_image_path = "static/AlmostMe.png"
    output_path = "static/generated.png"

    if not os.path.exists(base_image_path):
        return None

    img = Image.open(base_image_path).convert("RGBA")
    draw = ImageDraw.Draw(img)

    # Simula apertura de boca (muy básica)
    if "a" in text.lower():
        draw.ellipse((140, 240, 180, 260), fill="black")

    img.save(output_path)
    return "generated.png"
