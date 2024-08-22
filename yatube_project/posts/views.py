from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm
from .models import Post, Group, User


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


@login_required
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, 'posts/group_posts.html', context)


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)

    context = {
        'user_name': user.username,
        'total_posts': posts.count(),
        'user_posts_url': f'/profile/{username}',
        'posts': posts
    }
    return render(request, 'posts/profile.html', context)


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    context = {
        'user_name': post.author.username,
        'post_date': post.pub_date,
        'post_content': post.text,
        'post_detail_url': f'/posts/{post_id}',
        'group_posts_url': '/group/posts'
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', username=request.user.username)
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})