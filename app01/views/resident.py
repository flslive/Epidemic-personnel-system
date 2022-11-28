from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from django.http import JsonResponse
from app01.utils.pagination import Pagination
from app01.utils.form import ResidentModelForm, ResidentEditModelForm


def resident_list(request):
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data

    queryset = models.Resident.objects.filter(**data_dict).order_by('-category')

    page_object = Pagination(request, queryset, page_size=10)
    context = {'queryset': page_object.page_queryset,
               'page_string': page_object.html(),
               'search_data': search_data}

    return render(request, 'resident_list.html', context)


def resident_add(request):
    if request.method == 'GET':
        form = ResidentModelForm()
        context = {'title': '新建住户', 'form': form}
        return render(request, 'resident_add.html', context)

    form = ResidentModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/resident/list/')
    return render(request, 'resident_add.html', {'title': '新建住户', 'form': form})


def resident_edit(request, nid):
    row_object = models.Resident.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/resident/list/')

    if request.method == 'GET':
        form = ResidentEditModelForm(instance=row_object)
        return render(request, 'resident_edit.html', {'form': form})

    form = ResidentEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/resident/list/')
    return render(request, 'resident_edit.html', {'form': form})


def resident_delete(request, nid):
    models.Resident.objects.filter(id=nid).delete()
    return redirect('/resident/list/')


def chart_list(request):
    return render(request, 'chart_list.html')


def chart_bar(request):
    # 构造柱状图的数据

    num1 = models.Resident.objects.filter(category__contains='1').count()  # 阴性人员个数
    num2 = models.Resident.objects.filter(category__contains='2').count()  # 次密接者个数
    num3 = models.Resident.objects.filter(category__contains='3').count()  # 密接者个数
    num4 = models.Resident.objects.filter(category__contains='4').count()  # 阳性人员个数

    legend = ['住户']
    series_list = [
        {
            'name': '人员类别',
            'type': 'bar',
            'data': [num1, num2, num3, num4]
        },
    ]
    x_axis = ['阴性人员', '次密接者', '密接者', '阳性人员']

    result = {
        'status': True,
        'data': {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)


def chart_pie(request):
    num1 = models.Nurse.objects.count()
    num2 = models.Resident.objects.count()
    db_data_list = [
        {'value': num1, 'name': '医护人员'},
        {'value': num2, 'name': '住户'},
    ]
    result = {
        'status': True,
        'data': db_data_list
    }
    return JsonResponse(result)


def chart_line(request):
    num1 = models.Resident.objects.filter(category__contains='4').filter(building__contains='1').count()
    num2 = models.Resident.objects.filter(category__contains='4').filter(building__contains='2').count()
    num3 = models.Resident.objects.filter(category__contains='4').filter(building__contains='3').count()
    num4 = models.Resident.objects.filter(category__contains='4').filter(building__contains='4').count()

    legend = ['阳性']
    series_list = [
        {
            'name': '阳性',
            'type': 'line',
            'stack': 'Total',
            'data': [num1, num2, num3, num4]
        },
    ]
    x_axis = ['1号楼', '2号楼', '3号楼', '4号楼']

    result = {
        'status': True,
        'data': {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)
