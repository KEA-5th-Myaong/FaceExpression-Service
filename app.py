import cv2
import dlib
import numpy as np
import base64
import re
from flask import Flask, request, jsonify
from keras.models import load_model
from flask_cors import CORS

# Flask 애플리케이션 생성
app = Flask(__name__)
CORS(app)  # CORS 설정 추가

# 얼굴 인식
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 표정 인식을 위한 눈, 코, 입 등의 위치 반환
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# 표정 라벨링
expression_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# 표정 가중치 모델
model = load_model('emotion_model.hdf5', compile = False)

# 이미지 데이터 처리 함수
def analyze_expression(image_data):
    # 이미지 데이터 디코딩
    image_data = re.sub('^data:image/.+;base64,', '', image_data)
    image = np.frombuffer(base64.b64decode(image_data), np.uint8)
    frame = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # 얼굴 인식을 위해 회색조 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 얼굴 인식
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # 얼굴이 인식되지 않을 경우
    if len(faces) == 0:
        return "No face detected"

    # 얼굴이 인식되면 표정을 인식
    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]
        face_roi = cv2.resize(face_roi, (64, 64))
        face_roi = np.expand_dims(face_roi, axis=-1)
        face_roi = np.expand_dims(face_roi, axis=0)
        face_roi = face_roi / 255.0

        # 모델을 통해 표정 분석
        output = model.predict(face_roi)[0]
        expression_index = np.argmax(output)
        expression_label = expression_labels[expression_index]
        return expression_label

# 표정 분석 요청 처리
@app.route('/analyze_expression', methods=['POST'])
def analyze_expression_route():
    data = request.get_json()
    image_data = data['image']
    expression = analyze_expression(image_data)

    if expression is not None:
        return jsonify({
            'success': True,
            'code': 'COMMON_2000',
            'message': 'OK',
            'data': {
                'expression': expression
            }
        })
    else:
        return jsonify({
            'success': False,
            'code': 'AI_5000',
            'message': 'AI 서버에서 문제가 발생했습니다.'
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

