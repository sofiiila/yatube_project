from django.shortcuts import render


def index(request):
    template = 'posts/index.html'
    title = 'Здравствуй, Рус! Гойда!'
    li = ['Пельмени', 'Борщ']
    p = 'Пельмени – знаменитое блюдо русской кухни, имеющее древние китайские, финно-угорские, тюркские и славянские корни.Современное название происходит от удмуртского «пельнянь» – «хлебное ухо». Аналоги пельменей существуют во многих кухнях мира.Вкус, сытность и удобство хранения сделали пельмени исключительно популярными,готовые пельмени можно купить в любом продуктовом магазине.'
    slug = 'group_posts'
    context = {
        'title': title,
        'li': li,
        'p': p,
        'slug': slug,
    }
    return render(request, template, context)


def group_posts(request, slug):
    context = {
        'slug': slug,
        'text': 'Здесь будет информация о группах проекта Yatube',
    }
    return render(request, 'posts/group_posts.html', context)
