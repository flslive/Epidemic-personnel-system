import base64
import os
import time
import cv2
import pyttsx3 as pyttsx
import datetime
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Epidemic_personnel_system.settings')
django.setup()
from django.shortcuts import render, redirect
from aip import AipFace
from app01 import models
from app01.utils.form import RegisterModelForm

APP_ID = ""
API_KEY = ""
SECRET_KEY = ""


client = AipFace(APP_ID, API_KEY, SECRET_KEY)

IMAGE_TYPE = 'BASE64'

# 人脸库 用户组
GROUP = 'face_01'

# 摄像头
cap = cv2.VideoCapture(0)

# 人脸级联分类器
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +
                                     'haarcascade_frontalface_default.xml')
# 人眼级联分类器
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +
                                    'haarcascade_eye.xml')


# 照相函数
def getimage():
    while (True):
        # 获取摄像头拍摄到的画面
        ret, frame = cap.read()
        faces = face_cascade.detectMultiScale(frame, 1.3, 5)
        img = frame
        # 用人脸级联分类器引擎在人脸区域进行脸部识别
        for (x, y, w, h) in faces:
            # 画出人脸框, 蓝色, 画笔宽度
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # 框选出人脸区域, 在人脸区域而不是全图中进行人眼检测, 节省计算资源
            face_area = img[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(face_area, 1.3, 15)
            # 用人眼级联分类器引擎在人脸区域进行人眼识别返回的 eyes 为眼睛坐标列表
            for (ex, ey, ew, eh) in eyes:
                # 画出人眼框, 绿色, 画笔宽度为 1
                cv2.rectangle(face_area, (ex, ey), (ex + ew, ey + eh),
                              (0, 255, 0), 1)

        cv2.imshow('Camera Frame', img)
        flag = cv2.waitKey(1)
        if flag == 13:
            output_path = os.path.join(
                "D:\\code\\Epidemic_personnel_system\\app01\\face\\getCamera.jpg")  # 默认情况下 os.path.join 的路径为当前路径
            cv2.imwrite(output_path, img)
            voicePrompt("已拍照, 请按 Esc 键完成识别 !")
            time.sleep(2)
        if flag == 27:
            break
        if cv2.getWindowProperty('Camera Frame', cv2.WND_PROP_VISIBLE) < 1:
            cap.release()
            cv2.destroyAllWindows()


def transimage():
    f = open('D:\\code\\Epidemic_personnel_system\\app01\\face\\getCamera.jpg', 'rb')
    img = base64.b64encode(f.read())
    return img


def voicePrompt(string):
    engine = pyttsx.init()
    engine.say(string)
    engine.runAndWait()


# 上传到百度api进行人脸匹配
def go_api(image):
    result = client.search(str(image, 'utf-8'), IMAGE_TYPE, GROUP)
    if result['error_msg'] == 'SUCCESS':
        name = result['result']['user_list'][0]['user_id']
        score = result['result']['user_list'][0]['score']
        if score > 80:
            if name == 'user_id':
                print("人脸匹配成功! 欢迎回家%s : " % name)
                time.sleep(1)
        else:
            voicePrompt("人脸匹配失败。")
            return 0
        current_time = time.asctime(time.localtime(time.time()))
        models.Record.objects.create(name=name, current_time=current_time)
        return 1
    if result['error_msg'] == 'pic not has face':
        voicePrompt("检测不到人脸。")
        time.sleep(3)
        return -1


if __name__ == '__main__':
    while True:
        print('\n\n--------------------------------------')
        voicePrompt("面向摄像头并按下回车键。")
        if True:
            getimage()
            img = transimage()
            go_api(img)
            voicePrompt("人脸匹配成功")
            time.sleep(2)
