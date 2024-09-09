from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from posts.models import Post, Group


class ViewsTemplateTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.group = Group.objects.create(title='Test Group', slug='test-group')
        self.other_group = Group.objects.create(title='Other Group', slug='other-group')
        self.post = Post.objects.create(
            text='Test post',
            author=self.user,
            group=self.group
        )

    def test_post_on_index_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.text)

    def test_post_on_group_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('posts:group_posts', kwargs={'slug': self.group.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.text)

    def test_post_on_profile_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('posts:profile', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('posts', response.context)
        self.assertIn(self.post, response.context['posts'])
        self.assertContains(response, self.post.text)

    def test_post_not_on_other_group_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('posts:group_posts', kwargs={'slug': self.other_group.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.post.text)

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
                self.client.login(username='testuser', password='testpassword')
                if view_name == 'posts:group_posts':
                    response = self.client.get(reverse(view_name, kwargs={'slug': 'test-group'}))
                elif view_name == 'posts:profile':
                    response = self.client.get(reverse(view_name, kwargs={'username': 'testuser'}))
                elif view_name == 'posts:post_detail':
                    response = self.client.get(reverse(view_name, kwargs={'post_id': self.post.id}))
                elif view_name == 'posts:post_create':
                    response = self.client.get(reverse(view_name))
                elif view_name == 'posts:post_edit':
                    response = self.client.get(reverse(view_name, kwargs={'post_id': self.post.id}))
                else:
                    response = self.client.get(reverse(view_name))

                self.assertEqual(response.status_code, 200)
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
                self.client.login(username='testuser', password='testpassword')
                if view_name == 'posts:group_posts':
                    response = self.client.get(reverse(view_name, kwargs={'slug': 'test-group'}))
                elif view_name == 'posts:profile':
                    response = self.client.get(reverse(view_name, kwargs={'username': 'testuser'}))
                elif view_name == 'posts:post_detail':
                    response = self.client.get(reverse(view_name, kwargs={'post_id': self.post.id}))
                elif view_name == 'posts:post_create':
                    response = self.client.get(reverse(view_name))
                elif view_name == 'posts:post_edit':
                    response = self.client.get(reverse(view_name, kwargs={'post_id': self.post.id}))
                else:
                    response = self.client.get(reverse(view_name))

                self.assertEqual(response.status_code, 200)
                for key, expected in context.items():
                    with self.subTest(key=key):
                        self.assertIn(key, response.context)
                        if expected is not True:
                            self.assertEqual(response.context[key], expected)
