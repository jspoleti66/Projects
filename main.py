from flask import Flask, render_template_string, request, send_file
from talkingface import TalkingFace
import os

app = Flask(__name__)
avatar_path = 'static/avatar.png'
outputs_path = 'static/outputs'
os.makedirs(outputs_path, exist_ok=True)

talker = TalkingFace(avatar_path)

HTML_PAGE = '''
<!doctype html>
<title>AlmostMe - Demo</title>
<h2>Animación básica del clon</h2>
<form method=post>
  <input name=text placeholder="Escribí un mensaje..." size=40>
  <input type=submit value="Generar">
</form>
{% if filename %}
  <h3>Resultado:</h3>
  <video width="320" height="320" controls autoplay loop>
    <source src="{{ url_for('static', filename='outputs/' + filename) }}" type="video/mp4">
  </video>
{% endif %}
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    filename = None
    if request.method == 'POST':
        text = request.form['text']
        filename = f"out.mp4"
        output_path = os.path.join(outputs_path, filename)
        talker.animate(text, output_path)
    return render_template_string(HTML_PAGE, filename=filename)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
