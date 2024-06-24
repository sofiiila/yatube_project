from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'pub_date')


admin.site.register(Post, PostAdmin)

