from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


def index(request):
    template = 'posts/index.html'
    return render(request, template)


def group_posts(request, slug):
    return HttpResponse(f'Tyt chota budet {slug}')
# Create your views here.
