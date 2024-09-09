from http import HTTPStatus
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class UsersURLTests(TestCase):
    def setUp(self):
        # неавторизован
        self.guest_client = Client()
        # авторизован
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.authorized_client = Client()
        self.authorized_client.login(username='testuser', password='12345')

    def test_all_users_get_access(self):
        urls = [
            ('users:login', {}, HTTPStatus.OK),
            ('users:signup', {}, HTTPStatus.OK)
        ]
        for name, kwargs, expected_status in urls:
            with self.subTest(name=name, kwargs=kwargs):
                response = self.authorized_client.get(reverse(name, kwargs=kwargs))
                self.assertEqual(response.status_code, expected_status)

    def test_authorized_access(self):
        urls = [
            ('users:logout', {}, HTTPStatus.OK),
            ('users:password_reset_form', {}, HTTPStatus.OK),
            ('users:password_change', {}, HTTPStatus.FOUND),
            ('users:password_change_done', {}, HTTPStatus.FOUND),
            ('users:password_reset_confirm', {'uidb64': 'test', 'token': 'test'}, HTTPStatus.OK),
            ('users:password_reset_complete', {}, HTTPStatus.OK)
        ]
        for name, kwargs, expected_status in urls:
            with self.subTest(name=name, kwargs=kwargs):
                response = self.authorized_client.get(reverse(name, kwargs=kwargs))
                self.assertEqual(response.status_code, expected_status)

    def test_templates(self):
        templates = {
            reverse('users:login'): 'users/login.html',
            reverse('users:signup'): 'users/signup.html',
            reverse('users:logout'): 'users/logged_out.html',
            reverse('users:password_reset_form'): 'users/password_reset_form.html',
            reverse('users:password_reset_confirm', kwargs={'uidb64': 'test', 'token': 'test'}): 'users/password_reset_confirm.html',
            reverse('users:password_reset_complete'): 'users/password_reset_complete.html'
        }

        for url, template in templates.items():
            with self.subTest(url=url, template=template):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_password_change_redirect(self):
        response = self.authorized_client.post(reverse('users:password_change'), {
            'old_password': '12345',
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123'
        })
        self.assertRedirects(response, reverse('users:password_change_done'))

    def test_password_change_done_status(self):
        response = self.authorized_client.get(reverse('users:password_change_done'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/password_change_done.html')
