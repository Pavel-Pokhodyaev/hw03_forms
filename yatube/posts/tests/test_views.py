from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

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

    def setUp(self):
        # Создаем авторизованный клиент
        self.guest_client = Client()
        self.user = User.objects.create_user(username='StasBasov')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_about_page_uses_1(self):
        """Проверка правильности исп. html-шаблонов во view-функциях """

        name_templates = {
            reverse('posts:profile',
                kwargs={'username': 'StasBasov'}
                ): 'posts/profile.html',
            reverse('posts:post_detail',
                kwargs={'post_id': self.post.id}
                ): 'posts/post_detail.html',

            reverse('posts:post_edit',
                kwargs={'post_id': self.post.id}
                ): 'posts/create_post.html',
                
            reverse('posts:index'
                ): 'posts/index.html',
            reverse('posts:post_create'
                ): 'posts/create_post.html',
            reverse('posts:group_list',
                kwargs={'slug': self.group.slug}
                ): 'posts/group_list.html',
        }
        for name, template in name_templates.items():
            with self.subTest(name=name):
                response = self.authorized_client.get(name)
                self.assertTemplateUsed(response, template,
                                        f'Ошибка html-шаблона при вызове {name}')
