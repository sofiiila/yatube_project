from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostsModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

        cls.posts = [cls.post]

    def test_models_have_correct_object_names(self):
        """Тест метода __str__ модели Post."""
        for post in self.posts:
            with self.subTest(post=post):
                expected_object_name = post.text[:15]
                self.assertEqual(str(post), expected_object_name)


class GroupModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем группы
        cls.groups = [
            Group.objects.create(
                title=f'Test Group {i}',
                slug=f'test-group-{i}',
                description=f'This is test group {i}.'
            ) for i in range(1, 4)
        ]

    def test_group_str(self):
        """Тест метода __str__ модели Group."""
        for group in self.groups:
            with self.subTest(group=group):
                expected_object_name = group.title
                self.assertEqual(str(group), expected_object_name)