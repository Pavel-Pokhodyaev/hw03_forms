from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import TestCase, Client


User = get_user_model()

class StaticPagesURLTests(TestCase):
    #Создаем неавторизованый клиент
    def setUp(self):
        self.guest_client = Client()

    def test_pages_about(self):
            """Проверка  доступа к страницам приложения about."""
            pages = ['/about/author/', '/about/tech/']
            for page in pages:
                with self.subTest(page=page):
                    response = self.guest_client.get(page)
                    self.assertEqual(response.status_code, HTTPStatus.OK,
                                     f'Ошибка доступа к странице {page}')

    def test_urls_about(self):
        """URL-адрес использует соответствующий шаблонприложения фищге."""
        templates_url_names = {
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html',
        }

        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template,
                                        f'Ошибка шаблона post при вызове {url}')


    