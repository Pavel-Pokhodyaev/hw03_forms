from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from posts.models import Group, Post
 
User = get_user_model()


class UsersURLTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем запись в БД для проверки доступности
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group,
        )
    
    #Создаем неавторизованый клиент
    def setUp(self):
        self.guest_client = Client()
        # Создаем пользователя
        self.user = User.objects.create_user(username='HasNoName')
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)

    def test_pages_for_all_users(self):
        """Проверка  доступа к страницам входа и регистрации."""
        pages = ['/auth/login/', '/auth/signup/', '/',
                '/about/author/', '/about/tech/',
                '/auth/logout/', '/group/test-slug/']
        for page in pages:
            with self.subTest(page=page):
                response = self.guest_client.get(page)
                self.assertEqual(response.status_code, HTTPStatus.OK,
                                 f'Ошибка доступа к странице {page}')
    
    def test_pages_for_authorized_client(self):
        """Проверка  доступа к  страницам Новой записи и Редактирования."""
        pages = ['/create/', '/auth/password_change_form/', '/profile/HasNoName/']
        for page in pages:
            with self.subTest(page=page):
                response = self.authorized_client.get(page)
                self.assertEqual(response.status_code, HTTPStatus.OK,
                                 f'Ошибка доступа к странице {page}')

    # Проверяем редиректы для неавторизованного пользователя
    def test_post_detail_url_redirect_anonymous(self):
        """Страница /posts/45/edit/ перенаправляет анонимного
        пользователя выдавая код 302.
        """
        response = self.guest_client.get('/posts/45/edit/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_post_detail_url_redirect_anonymous_on_admin_login(self):
        """Страница по адресу /posts/45/edit/ перенаправит анонимного
        пользователя на страницу логина.
        """
        #post_id = self.post.id
        response = self.client.get('/posts/44/edit/', follow=True)
        self.assertRedirects(
            response, ('/auth/login/?next=/posts/44/edit/'))

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        
        post_id = self.post.id
        templates_url_names = {
            '/': 'posts/index.html',
            '/group/test-slug/': 'posts/group_list.html',
            '/profile/HasNoName/': 'posts/profile.html',
            f'/posts/{post_id}/': 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
        }

        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template,
                                        f'Ошибка шаблона post при вызове {url}')


