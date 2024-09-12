from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from users.forms import CreationForm


class SignUpViewTest(TestCase):
    def test_signup_view(self):
        response = self.client.get(reverse('users:signup'))

        with self.subTest('status_code'):
            self.assertEqual(response.status_code, 200)

        with self.subTest('template_used'):
            self.assertTemplateUsed(response, 'users/signup.html')

        with self.subTest('context_form'):
            self.assertIsInstance(response.context['form'], CreationForm)


class CustomLogoutViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))

        with self.subTest('status_code'):
            self.assertEqual(response.status_code, 200)

        with self.subTest('template_used'):
            self.assertTemplateUsed(response, 'users/logged_out.html')

        with self.subTest('user_logged_out'):
            self.assertNotIn('_auth_user_id', self.client.session)

    def test_logout_view_post_request(self):
        response = self.client.post(reverse('logout'))

        with self.subTest('status_code'):
            self.assertEqual(response.status_code, 200)

        with self.subTest('template_used'):
            self.assertTemplateUsed(response, 'users/logged_out.html')

        with self.subTest('user_logged_out'):
            self.assertNotIn('_auth_user_id', self.client.session)
