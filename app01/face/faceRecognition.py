from aip import AipFace
from django.http import StreamingHttpResponse
import base64
import time
import cv2
import os
import pyttsx3 as pyttsx
from app01.views.config import *


# 创建一个客户端用以访问百度云
client = AipFace(APP_ID, API_KEY, SECRET_KEY)

# 图像编码方式
IMAGE_TYPE = 'BASE64'

# 人脸库-用户组
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

        # 实时展示效果画面
        cv2.imshow('Camera Frame', img)
        # 每 1 毫秒监听一次键盘动作
        flag = cv2.waitKey(1)
        if flag == 13:  # 按下回车键进行拍照
            output_path = os.path.join(
                "getCamera.jpg")  # 默认情况下 os.path.join 的路径为当前路径
            cv2.imwrite(output_path, img)
            voicePrompt("已拍照, 请按 Esc 键退出拍照进入人脸验证环节 !")
            time.sleep(2)
        if flag == 27:  # 按下 ESC 键退出拍照
            break


# 对图片的格式进行转换
def transimage():
    f = open('getCamera.jpg', 'rb')
    img = base64.b64encode(f.read())
    return img


# 语音提示系统
def voicePrompt(string):
    engine = pyttsx.init()
    engine.say(string)
    engine.runAndWait()


# 上传到百度api进行人脸检测
def go_api(image):
    result = client.search(str(image, 'utf-8'), IMAGE_TYPE, GROUP)
    # 在百度云人脸库中寻找有没有匹配的人脸
    if result['error_msg'] == 'SUCCESS':  # 如果成功了
        name = result['result']['user_list'][0]['user_id']  # 获取名字
        score = result['result']['user_list'][0]['score']  # 获取相似度
        if score > 80:  # 如果相似度大于80
            if name == 'user_id':
                print("人脸匹配成功! 欢迎回家%s : " % name)
                time.sleep(1)
        else:
            voicePrompt("人脸匹配失败。")
            name = 'Unknow'
            return 0
        curren_time = time.asctime(time.localtime(time.time()))  # 获取当前时间
        # 将人员出入的记录保存到Log.txt中
        f = open('../views/Log.txt', 'a')
        f.write("Person: " + name + "     " + "Time:" + str(curren_time) +
                '\n')
        f.close()
        return 1
    if result['error_msg'] == 'pic not has face':
        voicePrompt("检测不到人脸。")
        time.sleep(3)
        return -1

    else:
        print(result['error_code'] + ' ' + result['error_code'])
        return 0


def gen_display(camera):
    while True:
        # 读取图片
        ret, frame = camera.read()
        if ret:
            frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # 将图片进行解码
            ret, frame = cv2.imencode('.jpeg', frame)
            if ret:
                # 转换为byte类型的，存储在迭代器中
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')


def video(request):
    # 视频流相机对象
    camera = cv2.VideoCapture(0)
    # 使用流传输传输视频流
    return StreamingHttpResponse(gen_display(camera), content_type='multipart/x-mixed-replace; boundary=frame')


# 主函数
if __name__ == '__main__':
    while True:
        print('\n\n--------------------------------------')
        voicePrompt("面向摄像头并按下回车键。")
        if True:
            getimage()  # 拍照
            img = transimage()  # 转换照片格式
            res = go_api(img)  # 将转换了格式的图片上传到百度云
            if (res == 1):  # 是人脸库中的人
                voicePrompt("人脸比对成功,欢迎回家 !")
            voicePrompt("即将进入下一次拍照验证环节 !")
            time.sleep(2)
