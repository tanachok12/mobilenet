from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import numpy as np
from PIL import Image
from io import BytesIO

app = Flask(__name__)
model = load_model('model/mobile_net_model.h5')

@app.route('/')
def index():
    return render_template('index.html')  # ตรวจสอบให้แน่ใจว่าไฟล์ index.html อยู่ในโฟลเดอร์ 'templates'
@app.route('/coffeemobilenet')
def coffeemobilenet():
    # This will render the coffeemobilenet.html template
    return render_template('coffeemobilenet.html')

@app.route('/carmobilenet')
def carmobilenet():
    # This will render the carmobilenet.html template
    return render_template('carmobilenet.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' in request.files:
        img_file = request.files['image']
        img_bytes = BytesIO(img_file.read())  # แปลงเป็น BytesIO
        img = Image.open(img_bytes)
        img = img.resize((224, 224))  # ปรับขนาดภาพ
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        predictions = model.predict(img_array)
        result = 'good' if predictions[0][0] > 0.5 else 'bad'

        return jsonify({'prediction': result})
    else:
        return jsonify({'error': 'No image provided'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5001)
