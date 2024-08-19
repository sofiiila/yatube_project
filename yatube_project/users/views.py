from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.views.generic import CreateView

from django.urls import reverse_lazy

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm

    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


class PasswordReset(PasswordResetView):
    template_name = 'users/password_reset_form.html'
    success_url = '/auth/password_reset/done/'

