"""Epidemic_personnel_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01.views import index, admin, account, nurse, resident, area, notice, face_register, face_updater
from app01.views import face, record

urlpatterns = [
    path('index/', index.index),

    path('admin/list/', admin.admin_list),
    path('admin/add/', admin.admin_add),
    path('admin/<int:nid>/edit/', admin.admin_edit),
    path('admin/<int:nid>/delete/', admin.admin_delete),
    path('admin/<int:nid>/reset/', admin.admin_reset),

    path('login/', account.login),
    path('logout/', account.logout),
    path('image/code/', account.image_code),

    path('nurse/list/', nurse.nurse_list),
    path('nurse/add/', nurse.nurse_add),
    path('nurse/<int:nid>/edit/', nurse.nurse_edit),
    path('nurse/<int:nid>/delete/', nurse.nurse_delete),

    path('resident/list/', resident.resident_list),
    path('resident/add/', resident.resident_add),
    path('resident/<int:nid>/edit/', resident.resident_edit),
    path('resident/<int:nid>/delete/', resident.resident_delete),

    path('area/list/', area.area_list),
    path('area/add/', area.area_add),
    path('area/delete/', area.area_delete),
    path('area/detail/', area.area_detail),
    path('area/edit/', area.area_edit),

    path('notice/list/', notice.notice_list),
    path('notice/add/', notice.notice_add),
    path('notice/<int:nid>/detail/', notice.notice_detail),
    path('notice/<int:nid>/edit/', notice.notice_edit),
    path('notice/<int:nid>/delete/', notice.notice_delete),

    path('chart/list/', resident.chart_list),
    path('chart/bar/', resident.chart_bar),
    path('chart/pie/', resident.chart_pie),
    path('chart/line/', resident.chart_line),

    path('face/regist/', face.regist),
    path('face/list/', face.face_list),
    path('face/record/', face.face_record),
    path('face/<int:nid>/edit/', face.face_edit),

    path('record/list/', record.record_list)

]
