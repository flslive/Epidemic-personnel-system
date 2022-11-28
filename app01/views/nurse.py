from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import NurseModelForm, NurseEditModelForm


def nurse_list(request):
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data

    queryset = models.Nurse.objects.filter(**data_dict).order_by('building')

    page_object = Pagination(request, queryset, page_size=5)
    context = {'queryset': page_object.page_queryset,
               'page_string': page_object.html(),
               'search_data': search_data}

    return render(request, 'nurse_list.html', context)


def nurse_add(request):
    if request.method == 'GET':
        form = NurseModelForm()
        context = {'title': '新建医护人员', 'form': form}
        return render(request, 'nurse_add.html', context)

    form = NurseModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/nurse/list/')
    return render(request, 'nurse_add.html', {'title': '新建医护人员', 'form': form})


def nurse_edit(request, nid):
    row_object = models.Nurse.objects.filter(id=nid).first()
    if not row_object:
        # return render(request,'error.html',{'msg':'数据不存在'})
        return redirect('/nurse/list/')

    if request.method == 'GET':
        form = NurseEditModelForm(instance=row_object)
        return render(request, 'nurse_edit.html', {'form': form})

    form = NurseEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/nurse/list/')
    return render(request, 'nurse_edit.html', {'form': form})


def nurse_delete(request, nid):
    models.Nurse.objects.filter(id=nid).delete()
    return redirect('/nurse/list/')
