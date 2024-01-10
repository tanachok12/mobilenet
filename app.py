from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
from PIL import Image
from io import BytesIO
import base64

# กำหนดค่าเบื้องต้นสำหรับ Flask app
app = Flask(__name__)
model = load_model('model/mobile_net_model.h5')
model2 = load_model('model/mobile_net_car_model.h5')

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
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        # ทำนายผล
        predictions = model.predict(img_array) # ใช้โมเดลที่ต้องการทำนาย

        # ตรวจสอบค่า threshold และทำนายคลาส
        threshold = float(request.form.get('threshold', 0.8))  # ค่าเริ่มต้นคือ 0.8
        predicted_class = np.argmax(predictions[0])
        predicted_prob = predictions[0][predicted_class]
        
        # กำหนดป้ายกำกับคลาส (ปรับตามโมเดล)
        class_labels = {
             0: 'Bad', 1: 'Good'
        }

        # คำนวณผลลัพธ์
        result = "Uncertain"
        if predicted_prob >= threshold:
            result = class_labels[predicted_class]
        probabilities = {class_labels[i]: str(prob * 100) for i, prob in enumerate(predictions[0])}

        # แปลงรูปภาพเป็น Base64
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # ส่งกลับผลทำนายและข้อมูลภาพ
        return jsonify({
            'prediction': result,
            'probability': str(predicted_prob),
            'class_probabilities': probabilities,  # ส่งกลับค่าความน่าจะเป็นสำหรับทุกคลาส
            'image_data': img_str,
            'threshold_used': threshold
        })
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
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        # ทำนายผล
        predictions = model2.predict(img_array)

        # ตรวจสอบค่า threshold และทำนายคลาส
        threshold = float(request.form.get('threshold', 0.5))  # ค่าเริ่มต้นคือ 0.3
        predicted_class = np.argmax(predictions[0])
        predicted_prob = predictions[0][predicted_class]
        
        # กำหนดป้ายกำกับคลาส
        class_labels = {
            0: 'Acura', 1: 'Audi', 2: 'BMW', 3: 'Chevrolet', 4: 'Ford',
            5: 'Honda', 6: 'Hyundai', 7: 'Infiniti', 8: 'KIA', 9: 'Lamborghini',
            10: 'Lexus', 11: 'Mazda', 12: 'MercedesBenz', 13: 'Nissan', 14: 'Porsche',
            15: 'Tesla', 16: 'Toyota', 17: 'Volkswagen'
        }

        # คำนวณผลลัพธ์
        result = "Uncertain"
        if predicted_prob >= threshold:
            result = class_labels[predicted_class]
        probabilities = {class_labels[i]: str(prob * 100) for i, prob in enumerate(predictions[0])}

        # แปลงรูปภาพเป็น Base64
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # ส่งกลับผลทำนายและข้อมูลภาพ
        return jsonify({
            'prediction': result,
            'probability': str(predicted_prob),
            'class_probabilities': probabilities,  # ส่งกลับค่าความน่าจะเป็นสำหรับทุกคลาส
            'image_data': img_str,
            'threshold_used': threshold
        })
    else:
        return jsonify({'error': 'No image provided'}), 400
# รัน Flask app
if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5001)
