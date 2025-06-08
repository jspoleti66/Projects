
from flask import Flask, render_template, request
import os
from inference import animate_from_text

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/", methods=["GET", "POST"])
def index():
    result_img = None
    if request.method == "POST":
        text = request.form["user_text"]
        result_img = animate_from_text(text)
    return render_template("index.html", result_img=result_img)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
