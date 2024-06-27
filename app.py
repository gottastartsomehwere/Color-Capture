from flask import Flask, render_template, request, send_file
import cv2
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    image_file = request.files['image']
    color_hex = request.form['color']
    color_bgr = tuple(int(color_hex[i:i+2], 16) for i in (5, 3, 1))
    image = Image.open(image_file.stream)
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_bound = np.array([color_bgr[0] - 10, 100, 100])
    upper_bound = np.array([color_bgr[0] + 10, 255, 255])
    mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
    result = cv2.bitwise_and(image, image, mask=mask)
    _, buffer = cv2.imencode('.jpg', result)
    io_buf = io.BytesIO(buffer)
    return send_file(io_buf, mimetype='image/jpeg')

if __name__ == '__main__': 
   app.run(host='0.0.0.0', debug=True)