from asyncio import sleep
from datetime import date
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms
from posts.models import Group, Post, User

User = get_user_model()

class TaskPagesTests(TestCase):

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

        for i in range(15, 0, -1):
            Post.objects.create(
                text = f'{i} numder post',
                author = cls.user,
                group = cls.group
                )
            sleep(1E-6)


       # cls.post = Post.objects.create(
            #text = f'Тестовый пост2',
            #author = cls.user,
            #pub_date = date.today(),
            #group = cls.group
            #)

    def setUp(self):
        # Создаем авторизованный клиент
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_about_page_uses_1(self):
        """Проверка правильности исп. html-шаблонов во view-функциях """

        name_templates = {
            reverse('posts:profile',
                kwargs={'username': 'auth'}
                ): 'posts/profile.html',
            reverse('posts:post_detail',
                kwargs={'post_id': self.post.id}
                ): 'posts/post_detail.html',
            reverse('posts:post_edit',
                kwargs={'post_id': self.post.id}
                ): 'posts/create_post.html',
            reverse('posts:index'
                ): 'posts/index.html',
            reverse('posts:create_post', 
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

# Проверка словаря контекста главной страницы (в нём передаётся форма)
    def test_home_page_show_correct_context(self):
        """Шаблон home сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        post = context['page'][0]
        self.assertEqual(post.author, TaskPagesTests.user)
        self.assertEqual(post.pub_date, TaskPagesTests.post.pub_date)
        self.assertEqual(post.text, TaskPagesTests.post.text)
        self.assertEqual(post.group, TaskPagesTests.post.group)

