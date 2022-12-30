from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import AdminModelForm, AdminEditModelForm, AdminResetModelForm


def admin_list(request):
    data_dict = {}  # 用于存放搜索条件
    search_data = request.GET.get('q', "")  # 搜索条件
    if search_data:
        data_dict["username__contains"] = search_data   # 搜索条件存放到字典中

    queryset = models.Admin.objects.filter(**data_dict)     # 搜索条件传递到数据库中

    page_object = Pagination(request, queryset, page_size=2)    # 分页
    context = {'queryset': page_object.page_queryset,
               'page_string': page_object.html(),
               'search_data': search_data}  # 数据传递到前端

    return render(request, 'admin_list.html', context)  # 返回数据


def admin_add(request):  # 添加管理员
    if request.method == 'GET':  # 如果是GET请求
        form = AdminModelForm()
        context = {'title': '新建管理员', 'form': form}  # 数据传递到前端
        return render(request, 'admin_add.html', context)   # 返回数据

    form = AdminModelForm(data=request.POST)    # 如果是POST请求
    if form.is_valid():  # 如果数据合法
        form.save()  # 保存数据到数据库
        return redirect('/admin/list/')  # 跳转到管理员列表
    return render(request, 'admin_add.html', {'title': '新建管理员', 'form': form})  # 返回数据


def admin_edit(request, nid):   # 编辑管理员
    row_object = models.Admin.objects.filter(id=nid).first()    # 获取当前管理员的信息
    if not row_object:  # 如果没有当前管理员
        return redirect('/admin/list/')     # 重定向到管理员列表

    if request.method == 'GET':     # 如果是GET请求
        form = AdminEditModelForm(instance=row_object)
        return render(request, 'admin_edit.html', {'form': form})

    form = AdminEditModelForm(data=request.POST, instance=row_object)   # 如果是POST请求
    if form.is_valid():     # 如果数据合法
        form.save()     # 保存数据到数据库
        return redirect('/admin/list/')     # 重定向至管理员列表
    return render(request, 'admin_edit.html', {'form': form})   # 返回数据


def admin_delete(request, nid):     # 删除管理员
    models.Admin.objects.filter(id=nid).delete()    # 在数据库中删除管理员
    return redirect('/admin/list/')     # 重定向至管理员列表


def admin_reset(request, nid):  # 重置管理员密码
    row_object = models.Admin.objects.filter(id=nid).first()    # 获取当前管理员的信息
    if not row_object:  # 如果没有当前管理员
        return redirect('/admin/list/')     # 重定向至管理员列表

    title = '重置用户 [ {} ] 的密码'.format(row_object.username)   # 重置密码的标题

    if request.method == 'GET':     # 如果是GET请求
        form = AdminResetModelForm()
        return render(request, 'admin_add.html', {'form': form, 'title': title})

    form = AdminResetModelForm(data=request.POST, instance=row_object)  # 如果是POST请求
    if form.is_valid():
        form.save()     # 保存数据到数据库
        return redirect('/admin/list/')
    return render(request, 'admin_add.html', {'form': form, 'title': title})    # 返回数据
