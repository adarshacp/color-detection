from flask import Flask, render_template, request, redirect, url_for
import os
import cv2
import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Load the color data
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

def get_color_name(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Load the image with OpenCV
        img = cv2.imread(filepath)
        # Resize or process the image if needed, then extract color
        # For example, get the color of the center pixel
        height, width, _ = img.shape
        center_color = img[height // 2, width // 2]
        b, g, r = center_color  # OpenCV uses BGR format

        # Get the color name
        color_name = get_color_name(r, g, b)

        return render_template('index.html', image_url=filename, color_name=color_name, rgb_values=f"R={r}, G={g}, B={b}")

if __name__ == '__main__':
    app.run(debug=True)
