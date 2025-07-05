from flask import Flask, render_template, request, jsonify
from fer import FER
import numpy as np
import cv2
import base64

app = Flask(__name__)
detector = FER()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json['image']
    encoded_data = data.split(',')[1]
    img_data = base64.b64decode(encoded_data)
    np_arr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    emotion, score = detector.top_emotion(img)
    response = {'emotion': emotion if emotion else 'No face', 'score': round(score, 2) if score else 0}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
