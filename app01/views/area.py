import json
import random
from datetime import datetime
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from app01.utils.form import AreaModelForm
from app01 import models
from app01.utils.pagination import Pagination


def area_list(request):
    queryset = models.Area.objects.all().order_by('id')
    page_object = Pagination(request, queryset, page_size=10)
    form = AreaModelForm()
    context = {
        'form': form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }
    return render(request, 'area_list.html', context)


@csrf_exempt
def area_add(request):
    form = AreaModelForm(data=request.POST)
    if form.is_valid():
        # 增加最后四位随机数
        form.instance.camera_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(1000, 9999))
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def area_delete(request):
    uid = request.GET.get('uid')
    exists = models.Area.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({'status': False, 'error': '删除失败，数据不存在'})

    models.Area.objects.filter(id=uid).delete()
    return JsonResponse({'status': True})


def area_detail(request):
    uid = request.GET.get('uid')
    row_dict = models.Area.objects.filter(id=uid).values('gate', 'building', 'floor', 'lift', 'household').first()
    if not row_dict:
        return JsonResponse({'status': False, 'error': '删除失败，数据不存在'})

    result = {
        'status': True,
        'data': row_dict
    }
    return JsonResponse(result)


@csrf_exempt
def area_edit(request):
    uid = request.GET.get('uid')
    row_object = models.Area.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({'status': False, 'tips': '删除失败，数据不存在'})

    form = AreaModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})
