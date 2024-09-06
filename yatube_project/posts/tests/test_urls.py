from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class StaticURLTests(TestCase):
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
        self.assertEqual(response.status_code, 200)

    def test_group_posts_authorized(self):
        response = self.authorized_client.get(reverse('posts:group_posts', kwargs={'slug': 'test-group'}))
        self.assertEqual(response.status_code, 200)

    def test_profile_authorized(self):
        response = self.authorized_client.get(reverse('posts:profile', kwargs={'username': 'testuser'}))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_authorized(self):
        response = self.authorized_client.get(reverse('posts:post_detail', kwargs={'post_id': self.post.id}))
        self.assertEqual(response.status_code, 200)

    def test_post_create_authorized(self):
        response = self.authorized_client.get(reverse('posts:post_create'))
        self.assertEqual(response.status_code, 200)

    def test_post_edit_authorized(self):
        response = self.authorized_client.get(reverse('posts:post_edit', kwargs={'post_id': self.post.id}))
        self.assertEqual(response.status_code, 200)

    def test_group_posts_redirect(self):
        response = self.guest_client.get(reverse('posts:group_posts', kwargs={'slug': 'test-group'}))
        self.assertRedirects(response, f'/auth/login/?next=/group/test-group/')

    def test_profile_redirect(self):
        response = self.guest_client.get(reverse('posts:profile', kwargs={'username': 'testuser'}))
        self.assertRedirects(response, f'/auth/login/?next=/profile/testuser/')

    def test_post_detail_redirect(self):
        response = self.guest_client.get(reverse('posts:post_detail', kwargs={'post_id': self.post.id}))
        self.assertRedirects(response, f'/auth/login/?next=/posts/{self.post.id}/')

    def test_post_create_redirect(self):
        response = self.guest_client.get(reverse('posts:post_create'))
        self.assertRedirects(response, f'/auth/login/?next=/create/')

    def test_post_edit_redirect(self):
        response = self.guest_client.get(reverse('posts:post_edit', kwargs={'post_id': self.post.id}))
        self.assertRedirects(response, f'/auth/login/?next=/posts/{self.post.id}/edit/')

