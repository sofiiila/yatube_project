from django.shortcuts import render, get_object_or_404
import datetime

from .models import Post, Group, User


def index(request):
    keyword = "утро"
    start_date = datetime.date(1854, 7, 7)
    end_date = datetime.date(1854, 7, 21)
    posts = Post.objects.filter(text__contains=keyword).filter(author=User.objects.get(username="leo")).filter(pub_date__range=(start_date, end_date))
    return render(request, "posts/index.html", {"posts": posts})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, 'posts/group_posts.html', context)
