import os
from flask import Flask, flash, request, redirect, url_for, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np

# 人脸识别
import cv2
import os

# 设置文件上传地址
IDENTIFY_UPLOAD_FOLDER = '../static/upload/identifyModel'
MODEL_UPLOAD_FOLDER = '../static/upload/faceModel'
# 允许上传的文件类型
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
# 初始化识别器
recognizer = cv2.face.LBPHFaceRecognizer_create()
# 人脸训练集路径
path = '../static/upload/faceModel'
# 获取分类器
faceCascade = cv2.CascadeClassifier(r'../static/data/haarcascade_frontalface_default.xml')
# 训练集合文件
trainerPath = '../trainer/trainer.yml'

# flask ---
app = Flask(__name__)
# 设置app属性
app.config['IDENTIFY_UPLOAD_FOLDER'] = IDENTIFY_UPLOAD_FOLDER
app.config['MODEL_UPLOAD_FOLDER'] = MODEL_UPLOAD_FOLDER
# 设置返回集合
data_false = {"isSuccess": False}
data_true = {"isSuccess": True}


# 获取允许的文件类型
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 人脸识别函数
@app.route('/face/identify', methods=['GET', 'POST'])
def Face():
    # 校验方法类型
    if request.method == 'POST':
        # 校验文件是否合法
        if 'file' not in request.files:
            return jsonify(data_false, "file不存在")
        file = request.files['file']
        if file.filename == '':
            return jsonify(data_false, "文件名称为空")
        # 安全校验filename
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['IDENTIFY_UPLOAD_FOLDER'], filename))
            # 加载训练好的模型文件
            recognizer.read(trainerPath)
            # 图片地址
            fiPath = '../static/upload/identifyModel/' + filename
            # 获取图片
            img = cv2.imread(fiPath)
            # 图片灰度化
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # 检测人脸
            # 参数：
            # scaleFactor(比例因子)：图片缩放多少，minNeighbors:至少检测多少次，
            # minSize:当前检测区域的最小面积
            # maxSize:当前检测区域的最面积
            # faces = face_detector.detectMultiScale(gray)
            # scaleFactor=1.01, minNeighbors=3, maxSize = (33, 33), minSize = (28, 28)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.3,
                minNeighbors=5,
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            for (x, y, w, h) in faces:
                # 画一个矩形
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # predict()函数返回两个元素的数组：第一个元素是所识别 个体的标签， 第二个是置信度评分。
                idnum, confidence = recognizer.predict(gray[y:y + h, x:x + w])
                # 设置匹配指数
                score = int("{0}".format(round(100 - confidence)))
                # 匹配指数大于等于60即可验证通过人脸
                print("score++++:", score)
                if score > 60:
                    os.remove(fiPath)
                    return jsonify(data_true)
                else:
                    os.remove(fiPath)
                    return jsonify(data_false, "验证不通过")
    else:
        return jsonify(data_false, "请求方式不为POST")


# 获取图像及标签
@app.route("/face/model", methods=['GET', 'POST'])
def getImagesAndLabels():
    # 校验方法类型
    if request.method == 'POST':
        # 校验文件是否合法
        if 'file' not in request.files:
            return jsonify(data_false, "file不存在")
        file = request.files['file']
        if file.filename == '':
            return jsonify(data_false, "文件名称为空")
        # 安全校验filename
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['MODEL_UPLOAD_FOLDER'], filename))
            # join函数的作用
            imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
            faceSamples = []
            ids = []
            for imagePath in imagePaths:
                PIL_img = Image.open(imagePath).convert('L')
                img_numpy = np.array(PIL_img, 'uint8')
                # 图片按照user.id.序列.jpg排列
                id = int(os.path.split(imagePath)[-1].split(".")[1])
                faces = faceCascade.detectMultiScale(img_numpy)
                for (x, y, w, h) in faces:
                    faceSamples.append(img_numpy[y:y + h, x: x + w])
                    ids.append(id)
            recognizer.train(faceSamples, np.array(ids))
            print("Training...")
            recognizer.write(trainerPath)
            print("Done.")
            return jsonify(data_true)
    else:
        return jsonify(data_false, "请求方式不为POST")

# if __name__ == '__main__':
#     name, confidence = Face()
#     score = "{0}".format(round(100 - confidence))
#     print("name++++", name)
#     print("score++++", score)
#     cv2.destroyAllWindows()
#     raise SystemExit
