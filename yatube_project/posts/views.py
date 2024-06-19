from django.shortcuts import render


def index(request):
    template = 'posts/index.html'
    title = 'Здравствуй, Рус! Гойда!'
    context = {
        'title': title,
        'text': 'Это главная страница проекта Yatube',
    }
    return render(request, template, context)


def group_posts(request, slug):
    context = {
        'slug': slug,
        'text': 'Здесь будет информация о группах проекта Yatube'
    }
    return render(request, 'posts/group_posts.html', context)
