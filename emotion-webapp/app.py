import os
from flask import Flask, render_template, request
from deepface import DeepFace
import cv2
import numpy as np

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    emotion = None
    image_path = None

    if request.method == 'POST':
        file = request.files['image']
        if file:
            filename = file.filename
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(image_path)

            try:
                # Read image and analyze
                img = cv2.imread(image_path)
                result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
                emotion = result[0]['dominant_emotion']
            except Exception as e:
                emotion = f"Error: {str(e)}"

    return render_template('index.html', emotion=emotion, image=image_path)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


