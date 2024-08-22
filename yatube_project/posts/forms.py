from django import forms
from .models import CreatePost


class PostForm(forms.ModelForm):
    class Meta:
        model = CreatePost
        fields = ['text', 'group']