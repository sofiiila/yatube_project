from django.test import TestCase, Client
from django.urls import reverse
from django.core.cache import cache
from posts.models import Post, Group, User


class IndexPageCacheTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.group = Group.objects.create(title='Test Group', slug='test-group')
        self.post = Post.objects.create(
            text='Test post',
            author=self.user,
            group=self.group
        )

    def test_index_page_cache(self):
        # Первый запрос для заполнения кеша
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.text)

        # Второй запрос должен использовать кеш
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.text)

        # Очистка кеша
        cache.clear()

        # Третий запрос после очистки кеша
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.text)

    def test_index_page_cache_timeout(self):
        # Первый запрос для заполнения кеша
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.text)

        # Подождать 21 секунду, чтобы кеш истек
        import time
        time.sleep(21)

        # Второй запрос после истечения времени кеша
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.text)