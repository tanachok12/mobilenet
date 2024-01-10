from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import numpy as np
from PIL import Image
from io import BytesIO
import base64

# กำหนดค่าเบื้องต้นสำหรับ Flask app
app = Flask(__name__)
model = load_model('model/mobile_net_model.h5')
model2 = load_model('model/mobile_net_model.h5')

# หน้าแรก
@app.route('/')
def index():
    return render_template('index.html')

# หน้าสำหรับระบบทำนายกาแฟ
@app.route('/coffeemobilenet')
def coffeemobilenet():
    return render_template('coffeemobilenet.html')

# หน้าสำหรับระบบทำนายรถยนต์
@app.route('/carmobilenet')
def carmobilenet():
    return render_template('carmobilenet.html')

# Endpoint สำหรับทำนายภาพ
@app.route('/predict', methods=['POST'])
def predict():
    if 'image' in request.files:
        # รับไฟล์รูปภาพ
        img_file = request.files['image']
        img = Image.open(img_file.stream)  # อ่านไฟล์จาก stream

        # ประมวลผลภาพ
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img = img.resize((224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        # รับค่า threshold จากคำขอ (ถ้ามี)
        threshold = float(request.form.get('threshold', 0.8))  # ค่าเริ่มต้นคือ 0.8

        # ทำนายผลโดยใช้ค่า threshold ที่รับมา
        predictions = model.predict(img_array)
        result = 'good' if predictions[0][0] > threshold else 'bad'

        # แปลงรูปภาพเป็น Base64
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # ส่งกลับผลทำนายและข้อมูลภาพ
        return jsonify({'prediction': result, 'image_data': img_str, 'threshold_used': threshold})
    else:
        return jsonify({'error': 'No image provided'}), 400

@app.route('/predict2', methods=['POST'])
def predict2():
    if 'image' in request.files:
        # รับไฟล์รูปภาพ
        img_file = request.files['image']
        img = Image.open(img_file.stream)  # อ่านไฟล์จาก stream

        # ประมวลผลภาพ
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img = img.resize((224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        # รับค่า threshold จากคำขอ (ถ้ามี)
        threshold = float(request.form.get('threshold', 0.8))  # ค่าเริ่มต้นคือ 0.8

        # ทำนายผลโดยใช้ค่า threshold ที่รับมา
        predictions = model2.predict(img_array)
        result = 'good' if predictions[0][0] > threshold else 'bad'

        # แปลงรูปภาพเป็น Base64
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # ส่งกลับผลทำนายและข้อมูลภาพ
        return jsonify({'prediction': result, 'image_data': img_str, 'threshold_used': threshold})
    else:
        return jsonify({'error': 'No image provided'}), 400
# รัน Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5001)