from django.contrib.auth import logout
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm

    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return render(request, 'users/logged_out.html')

    def post(self, request, *args, **kwargs):
        logout(request)
        return render(request, 'users/logged_out.html')
