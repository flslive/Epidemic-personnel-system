from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from app01.utils.code import check_code
from io import BytesIO
from app01.utils.form import Loginform


def login(request):

    if request.method == "GET":
        form = Loginform()
        return render(request, 'login.html', {'form': form})

    form = Loginform(data=request.POST)
    if form.is_valid():
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', '')

        if code.upper() != user_input_code.upper():
            form.add_error('code', '验证码错误')
            return render(request, 'login.html', {'form': form})

        # 去数据库校验用户名和密码是否正确
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()

        if not admin_object:
            form.add_error('password', '用户名或密码错误')
            return render(request, 'login.html', {'form': form})

        # 生成随机字符串，写入到用户浏览器的 cookie 中，再写入到 session 中
        request.session['info'] = {'id': admin_object.id, 'name': admin_object.username}

        # session可以保存 1 天
        request.session.set_expiry(60 * 60 * 24)

        return redirect('/index/')
    return render(request, 'login.html', {'form': form})


def image_code(request):

    # 调用 pillow 函数生成图片
    img, code_string = check_code()

    # 用于验证码校验
    request.session['image_code'] = code_string

    # 给 session 设置 60s 超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):

    request.session.clear()
    return redirect('/login/')
