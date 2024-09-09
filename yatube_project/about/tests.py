from http import HTTPStatus
from django.test import TestCase, Client
from django.urls import reverse


class StaticPagesTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_tech_urls_exists_at_desired_location(self):
        """Проверка доступности адресов /about/author/ и /about/tech/."""
        urls = ['/about/author/', '/about/tech/']

        for url in urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_tech_pages_uses_correct_template(self):
        urls_templates = {
            'about:author': 'about/author.html',
            'about:tech': 'about/tech.html'
        }

        for url, template in urls_templates.items():
            with self.subTest(url=url):
                response = self.guest_client.get(reverse(url))
                self.assertTemplateUsed(response, template)

