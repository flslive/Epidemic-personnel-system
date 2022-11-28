import os
from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import RegisterModelForm


def regist(request):
    if request.method == 'GET':
        form = RegisterModelForm()
        context = {'form': form}
        return render(request, 'regist.html', context)

    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        os.system('D:\\code\\Epidemic_personnel_system\\app01\\views\\face_register.py')
        return redirect('/face/regist/')
    return render(request, 'regist.html', {'form': form})


def face_list(request):
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["head__contains"] = search_data

    queryset = models.Register.objects.filter(**data_dict)

    page_object = Pagination(request, queryset, page_size=10)
    context = {'queryset': page_object.page_queryset,
               'page_string': page_object.html(),
               'search_data': search_data}

    return render(request, 'face_list.html', context)


def face_edit(request, nid):
    row_object = models.Register.objects.filter(id=nid).first().head
    if not row_object:
        return redirect('/face/list/')

    title = '重新录入 [ {} ] 的人脸，按下更新键进行面部识别'.format(models.Register.objects.filter(id=nid).first().head)

    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'face_edit.html', {'form': form, 'title': title})
    form = RegisterModelForm(data=request.POST)
    if request.method == 'POST':
        os.system('D:\\code\\Epidemic_personnel_system\\app01\\views\\face_updater.py')
        return redirect('/face/list/')
    return render(request, 'face_edit.html', {'form': form, 'title': title}), row_object


def face_delete(request, nid):
    models.Register.objects.filter(id=nid).delete()
    return redirect('/face/list/')


def face_record(request):
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'face_record.html', {'form': form})
    form = RegisterModelForm(data=request.POST)
    if request.method == 'POST':
        os.system('D:\\code\\Epidemic_personnel_system\\app01\\views\\face_record.py')
        return redirect('/face/record/')
    return render(request, 'face_record.html', {'form': form})
