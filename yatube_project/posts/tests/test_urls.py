from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpResponseNotFound
from posts.models import Group, Post

User = get_user_model()


class PostsURLTests(TestCase):
    def setUp(self):
        # неавторизован
        self.guest_client = Client()
        # авторизован
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.authorized_client = Client()
        self.authorized_client.login(username='testuser', password='12345')

        self.group = Group.objects.create(
            title='Test Group',
            slug='test-group',
            description='Test Description'
        )
        self.post = Post.objects.create(
            text='Test Post',
            author=self.user,
            group=self.group
        )

    def test_homepage(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_authorized_access(self):
        urls = [
            ('posts:group_posts', {'slug': 'test-group'}, HTTPStatus.OK),
            ('posts:profile', {'username': 'testuser'}, HTTPStatus.OK),
            ('posts:post_detail', {'post_id': self.post.id}, HTTPStatus.OK),
            ('posts:post_create', {}, HTTPStatus.OK),
            ('posts:post_edit', {'post_id': self.post.id}, HTTPStatus.OK),
        ]

        for name, kwargs, expected_status in urls:
            with self.subTest(name=name, kwargs=kwargs):
                response = self.authorized_client.get(reverse(name, kwargs=kwargs))
                self.assertEqual(response.status_code, expected_status)

    def test_redirect_anonymous(self):
        urls = [
            ('posts:group_posts', {'slug': 'test-group'}, '/auth/login/?next=/group/test-group/'),
            ('posts:profile', {'username': 'testuser'}, '/auth/login/?next=/profile/testuser/'),
            ('posts:post_detail', {'post_id': self.post.id}, f'/auth/login/?next=/posts/{self.post.id}/'),
            ('posts:post_create', {}, '/auth/login/?next=/create/'),
            ('posts:post_edit', {'post_id': self.post.id}, f'/auth/login/?next=/posts/{self.post.id}/edit/'),
        ]

        for name, kwargs, redirect_url in urls:
            with self.subTest(name=name, kwargs=kwargs):
                response = self.guest_client.get(reverse(name, kwargs=kwargs))
                self.assertRedirects(response, redirect_url)

    def test_404_page(self):
        response = self.guest_client.get('/nonexistent-page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_templates(self):
        templates = {
            '/': 'posts/index.html',
            '/group/test-group/': 'posts/group_posts.html',
            '/profile/testuser/': 'posts/profile.html',
            f'/posts/{self.post.id}/': 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
            f'/posts/{self.post.id}/edit/': 'posts/create_post.html',
        }

        for url, template in templates.items():
            with self.subTest(url=url, template=template):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_404_template(self):
        response = self.guest_client.get('/nonexistent-page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateUsed(response, 'core/404.html')



