import json
import base64
from django.apps import AppConfig
from aip import AipFace
from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction
from django.views import View


class Appconfig(AppConfig):
    name = ''
    APP_ID = '26756829'
    API_KEY = 'u5wKSPbkHPsVPuYDOOPIllEw'
    SECRECT_KEY = '97fjsv505GGBaoo6ODwSQmASftVGjOsI'
    client = AipFace(APP_ID, API_KEY, SECRECT_KEY)
    client.setConnectionTimeoutInMillis(1000 * 5)
    client.setSocketTimeoutInMillis(1000 * 5)


class Regist(View):
    def get(self, request):
        return render(request, 'regist.html')

    def post(self, request):
        image_content = request.POST.get('image_content')
        username = request.POST.get('username')
        if not all([image_content, username]):
            return JsonResponse({'result': '注册信息不能为空'})
        else:
            try:
                # 引入事务
                with transaction.atomic():
                    # 分割字符串
                    base_data = image_content.split(',')[1]
                    # base64解码
                    base64_decode = base64.b64decode(base_data)
                    # 图片写入本地
                    with open('static/image/' + '.jpeg', 'wb') as f:
                        f.write(base64_decode)
                    imageType = 'BASE64'
                    groupId = 'face_01'  # 自定义
                    username = request.POST.get('username')
                    userId = username
                    # 加入可选参数
                    options = {}
                    options['user_info'] = username
                    options['quality_control'] = 'NORMAL'
                    options['liveness_control'] = 'LOW'
                    result = Appconfig.client.addUser(base_data, imageType, groupId, userId, options)
                    print(result)
                    error_code = result['error_code']
                    if isinstance(error_code, int) and error_code == 0:
                        return JsonResponse({'code': 200, 'result': '注册成功'})
            except:
                return JsonResponse({'result': '注册失败'})

