from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from posts.models import Post, Group


class ViewsTemplateTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.group = Group.objects.create(title='Test Group', slug='test-group')
        self.post = Post.objects.create(
            text='Test post',
            author=self.user,
            group=self.group
        )

    def test_templates_used(self):
        templates = {
            'posts:index': 'posts/index.html',
            'posts:group_posts': 'posts/group_posts.html',
            'posts:profile': 'posts/profile.html',
            'posts:post_detail': 'posts/post_detail.html',
            'posts:post_create': 'posts/create_post.html',
            'posts:post_edit': 'posts/create_post.html',
        }

        for view_name, template in templates.items():
            with self.subTest(view_name=view_name):
                if view_name == 'posts:group_posts':
                    self.client.login(username='testuser', password='testpassword')
                    response = self.client.get(reverse(view_name, kwargs={'slug': 'test-group'}))
                elif view_name == 'posts:profile':
                    self.client.login(username='testuser', password='testpassword')
                    response = self.client.get(reverse(view_name, kwargs={'username': 'testuser'}))
                elif view_name == 'posts:post_detail':
                    self.client.login(username='testuser', password='testpassword')
                    response = self.client.get(reverse(view_name, kwargs={'post_id': self.post.id}))
                elif view_name == 'posts:post_create':
                    self.client.login(username='testuser', password='testpassword')
                    response = self.client.get(reverse(view_name))
                elif view_name == 'posts:post_edit':
                    self.client.login(username='testuser', password='testpassword')
                    response = self.client.get(reverse(view_name, kwargs={'post_id': self.post.id}))
                else:
                    response = self.client.get(reverse(view_name))

                self.assertTemplateUsed(response, template)

    def test_context_data(self):
        contexts = {
            'posts:index': {'page_obj': True},
            'posts:group_posts': {'group': True, 'page_obj': True},
            'posts:profile': {'user_name': True, 'total_posts': True, 'user_posts_url': True, 'posts': True},
            'posts:post_detail': {'user_name': True, 'post_date': True, 'post_content': True, 'post_detail_url': True,
                                  'group_posts_url': True},
            'posts:post_create': {'form': True},
            'posts:post_edit': {'form': True, 'is_edit': True},
        }

        for view_name, context in contexts.items():
            with self.subTest(view_name=view_name):
                if view_name == 'posts:group_posts':
                    self.client.login(username='testuser', password='testpassword')
                    response = self.client.get(reverse(view_name, kwargs={'slug': 'test-group'}))
                elif view_name == 'posts:profile':
                    self.client.login(username='testuser', password='testpassword')
                    response = self.client.get(reverse(view_name, kwargs={'username': 'testuser'}))
                elif view_name == 'posts:post_detail':
                    self.client.login(username='testuser', password='testpassword')
                    response = self.client.get(reverse(view_name, kwargs={'post_id': self.post.id}))
                elif view_name == 'posts:post_create':
                    self.client.login(username='testuser', password='testpassword')
                    response = self.client.get(reverse(view_name))
                elif view_name == 'posts:post_edit':
                    self.client.login(username='testuser', password='testpassword')
                    response = self.client.get(reverse(view_name, kwargs={'post_id': self.post.id}))
                else:
                    response = self.client.get(reverse(view_name))

                for key, expected in context.items():
                    with self.subTest(key=key):
                        self.assertIn(key, response.context)
                        if expected is not True:
                            self.assertEqual(response.context[key], expected)
