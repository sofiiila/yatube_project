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

    def form_valid(self, form):
        user = form.save(commit=False)
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()
        return super().form_valid(form)


class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return render(request, 'users/logged_out.html')

    def post(self, request, *args, **kwargs):
        logout(request)
        return render(request, 'users/logged_out.html')
