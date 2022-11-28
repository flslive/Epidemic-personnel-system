from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect, HttpResponse


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 排除那些不需要登录就能访问的页面
        # request.path_info 获取当前用户请求的URL /login/
        if request.path_info in ["/login/", "/image/code/"]:
            return

        # 访问当前用户session信息，如果有说明登录过，继续向后走
        info_dict = request.session.get('info')
        if info_dict:
            return

        # 没有登录过,返回到登录页面
        return HttpResponse('请登录')
