from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from datetime import datetime

from posts.models import Post, Group

User = get_user_model()


class PaginatorPagesTest(TestCase):
    """Проверка страниц приложения posts с паджинатором."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="auth")
        cls.user_auth = Client()
        cls.user_auth.force_login(cls.user)
        cls.group = Group.objects.create(
            title="Тестовый заголовок",
            description="Тестовое описание",
            slug="test-slug",
        )
        cls.many_posts = []
        for i in range(12):
            cls.many_posts.append(
                Post.objects.create(
                    text="Тестовый пост длиннее 15 символов",
                    author=cls.user,
                    pub_date=datetime.now(),
                    group=cls.group,
                )
            )

    def test_paginator_obj(self):
        """Паджинатор выводит не более 10 постов странице."""
        pages = [
            reverse("posts:index"),
            reverse(
                "posts:profile", kwargs={"username": PaginatorPagesTest.user}
            ),
            reverse(
                "posts:group_posts",
                kwargs={"slug": PaginatorPagesTest.group.slug},
            ),
        ]
        for page in pages:
            with self.subTest(reverse=page):
                response = PaginatorPagesTest.user_auth.get(page)
                self.assertEqual(len(response.context["page_obj"]), 10)
                response = PaginatorPagesTest.user_auth.get(page + "?page=2")
                self.assertEqual(len(response.context["page_obj"]), 2)
