from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from posts.models import Post, Follow

User = get_user_model()


class FollowTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.client.login(username='user1', password='password1')

    def test_follow(self):
        response = self.client.post(reverse('posts:profile_follow', args=[self.user2.username]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Follow.objects.filter(user=self.user1, author=self.user2).exists())

    def test_unfollow(self):
        Follow.objects.create(user=self.user1, author=self.user2)
        response = self.client.post(reverse('posts:profile_unfollow', args=[self.user2.username]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Follow.objects.filter(user=self.user1, author=self.user2).exists())

    def test_follow_index(self):
        post = Post.objects.create(author=self.user2, text='Test post')
        Follow.objects.create(user=self.user1, author=self.user2)
        response = self.client.get(reverse('posts:follow_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.text)

    def test_follow_index_no_follow(self):
        post = Post.objects.create(author=self.user2, text='Test post')
        response = self.client.get(reverse('posts:follow_index'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, post.text)
