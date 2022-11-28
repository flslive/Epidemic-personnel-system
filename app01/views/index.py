from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from app01.utils.pagination import Pagination


# from app01.utils.form import


def index(request):
    return render(request, 'index.html')
