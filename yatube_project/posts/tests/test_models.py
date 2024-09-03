from django.test import TestCase

from yatube_project.posts.forms import PostForm
from yatube_project.posts.models import Group


class PostFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.group = Group.objects.create(name='Test Group')

    def test_good_case_valid_data(self):
        form_data = {
            'text': 'Текст нового поста',
            'group': self.group.id,
        }
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_bad_case_invalid_data(self):
        form_data = {
            'text': '',
            'group': self.group.id,
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors)
