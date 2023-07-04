# 人脸识别
import cv2
import os
import sys


# 人脸识别函数
def Face():
    # 初始化识别器
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    # 加载训练好的模型文件
    recognizer.read('../trainer/trainer.yml')
    # 获取分类器
    faceCascade = cv2.CascadeClassifier(r'../static/data/haarcascade_frontalface_default.xml')
    # 获取图片
    path = '../static/upload/identifyModel/q.1.2.jpg'
    img = cv2.imread(path)
    confidence = 150.00  # 设置置信度初始值
    name = "unknown"
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
        # 匹配指数大于等于95即可验证通过人脸
        if score > 60:
            print(True)
        else:
            print(False)

    os.remove(path)
    return name, confidence


if __name__ == '__main__':
    name, confidence = Face()
    score = "{0}".format(round(100 - confidence))
    print("name++++", name)
    print("score++++", score)
    cv2.destroyAllWindows()
    raise SystemExit
