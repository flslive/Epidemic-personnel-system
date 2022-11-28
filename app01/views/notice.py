from django.shortcuts import render, redirect, HttpResponse
from app01.utils.form import NoticeModelForm, NoticeEditModelForm, NoticeDetailModelForm
from app01 import models
from app01.utils.pagination import Pagination


def notice_list(request):
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["title__contains"] = search_data

    queryset = models.Notice.objects.filter(**data_dict)

    page_object = Pagination(request, queryset, page_size=10)
    context = {'queryset': page_object.page_queryset,
               'page_string': page_object.html(),
               'search_data': search_data}

    return render(request, 'notice_list.html', context)


def notice_add(request):
    if request.method == 'GET':
        form = NoticeModelForm()
        context = {'title': '新建公告', 'form': form}
        return render(request, 'notice_add.html', context)

    form = NoticeModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/notice/list/')
    return render(request, 'notice_add.html', {'title': '新建公告', 'form': form})


def notice_detail(request, nid):
    row_object = models.Notice.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/notice/list/')

    if request.method == 'GET':
        form = NoticeDetailModelForm(instance=row_object)
        return render(request, 'notice_detail.html', {'form': form})


def notice_edit(request, nid):
    row_object = models.Notice.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/notice/list/')

    if request.method == 'GET':
        form = NoticeEditModelForm(instance=row_object)
        return render(request, 'notice_edit.html', {'form': form})

    form = NoticeEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/notice/list/')
    return render(request, 'notice_edit.html', {'form': form})


def notice_delete(request, nid):
    models.Notice.objects.filter(id=nid).delete()
    return redirect('/notice/list/')
