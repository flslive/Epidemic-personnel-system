from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import AdminModelForm, AdminEditModelForm, AdminResetModelForm


def admin_list(request):
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["username__contains"] = search_data

    queryset = models.Admin.objects.filter(**data_dict)

    page_object = Pagination(request, queryset, page_size=2)
    context = {'queryset': page_object.page_queryset,
               'page_string': page_object.html(),
               'search_data': search_data}

    return render(request, 'admin_list.html', context)


def admin_add(request):
    if request.method == 'GET':
        form = AdminModelForm()
        context = {'title': '新建管理员', 'form': form}
        return render(request, 'admin_add.html', context)

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'admin_add.html', {'title': '新建管理员', 'form': form})


def admin_edit(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/admin/list/')

    if request.method == 'GET':
        form = AdminEditModelForm(instance=row_object)
        return render(request, 'admin_edit.html', {'form': form})

    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'admin_edit.html', {'form': form})


def admin_delete(request, nid):
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')


def admin_reset(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/admin/list/')

    title = '重置用户 [ {} ] 的密码'.format(row_object.username)

    if request.method == 'GET':
        form = AdminResetModelForm()
        return render(request, 'admin_add.html', {'form': form, 'title': title})

    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'admin_add.html', {'form': form, 'title': title})
