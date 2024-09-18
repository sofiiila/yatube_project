from django.test import TestCase, Client, override_settings
from django.urls import reverse
from posts.models import Post, Group, User


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.group = Group.objects.create(
            title='Test Group',
            slug='test-group',
            description='Test description'
        )
        for i in range(13):
            Post.objects.create(
                text=f'Test post {i}',
                author=cls.user,
                group=cls.group
            )

    def setUp(self):
        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_pagination(self):
        pages = {
            'posts:index': {},
            'posts:group_posts': {'slug': 'test-group'},
            'posts:profile': {'username': 'testuser'}
        }

        for view_name, kwargs in pages.items():
            with self.subTest(view_name=view_name):
                response = self.client.get(reverse(view_name, kwargs=kwargs))
                self.assertIn('page_obj', response.context)
                self.assertEqual(len(response.context['page_obj']), 10)

                response = self.client.get(reverse(view_name, kwargs=kwargs) + '?page=2')
                self.assertIn('page_obj', response.context)
                self.assertEqual(len(response.context['page_obj']), 3)
