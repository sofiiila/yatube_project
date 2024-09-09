from http import HTTPStatus
from django.test import TestCase, Client


class StaticPagesUrlTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_urls_exists_at_desired_location(self):
        """Проверка доступности адресов /about/author/ и /about/tech/."""
        urls = ['/about/author/', '/about/tech/']

        for url in urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
