from django.test import TestCase, Client
from django.urls import reverse
from posts.models import Post, Group
from django.contrib.auth import get_user_model

User = get_user_model()


class PostTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.group = Group.objects.create(title='Test Group', slug='test-group')
        self.client.login(username='testuser', password='testpassword')

    def test_create_post(self):
        form_data = {
            'text': 'Test post text',
            'group': self.group.id,
        }
        response = self.client.post(reverse('posts:post_create'), data=form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Post.objects.filter(text='Test post text').exists())

    def test_edit_post(self):
        post = Post.objects.create(text='Original text', group=self.group, author=self.user)
        form_data = {
            'text': 'Edited text',
            'group': self.group.id,
        }
        response = self.client.post(reverse('posts:post_edit', args=(post.id,)), data=form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        post.refresh_from_db()
        self.assertEqual(post.text, 'Edited text')
