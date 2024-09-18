from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from posts.models import Post, Comment

User = get_user_model()


class CommentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.post = Post.objects.create(
            text='Test post',
            author=self.user
        )
        self.add_comment_url = reverse('posts:add_comment', args=[self.post.id])
        self.post_detail_url = reverse('posts:post_detail', args=[self.post.id])

    def test_comment_unauth_user_redirect(self):
        response = self.client.post(self.add_comment_url, {'text': 'Test comment'})
        self.assertRedirects(response, f'/auth/login/?next={self.add_comment_url}')

    def test_comment_auth_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.add_comment_url, {'text': 'Test comment'})
        self.assertRedirects(response, self.post_detail_url)
        response = self.client.get(self.post_detail_url)
        self.assertContains(response, 'Test comment')
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().text, 'Test comment')