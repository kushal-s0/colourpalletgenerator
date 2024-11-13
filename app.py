from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
from collections import Counter
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit to 16 MB

def get_common_colors(image_path, n_colors=5):
    image = Image.open(image_path)
    image = image.resize((100, 100))  # Resize for faster processing
    image = image.convert("RGB")  # Ensure RGB format

    # Get all pixels as a list
    pixels = list(image.getdata())

    # Count each color occurrence
    color_counts = Counter(pixels)
    most_common_colors = color_counts.most_common(n_colors)

    # Convert RGB tuples to hex
    hex_colors = [f'#{r:02x}{g:02x}{b:02x}' for (r, g, b), _ in most_common_colors]
    return hex_colors

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]
        if file:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(image_path)
            colors = get_common_colors(image_path)
            return render_template("index.html", colors=colors, image_url=image_path)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
