from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse('Главная страница')


def group_posts(request, slug):
    return HttpResponse(f'Tyt chota budet {slug}')
# Create your views here.
