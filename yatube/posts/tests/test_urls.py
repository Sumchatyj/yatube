from django.test import TestCase, Client
from http import HTTPStatus
from posts.models import Group, Post, User


class URLTests(TestCase):
    """Проверка URL приложения posts."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="auth")
        cls.user_auth = Client()
        cls.user_auth.force_login(cls.user)
        cls.user_random = Client()
        cls.group = Group.objects.create(
            title="Тестовый заголовок",
            description="Тестовое описание",
            slug="test-slug",
        )
        cls.post = Post.objects.create(
            author=cls.user, text="Тестовый пост длиннее 15 символов", pk=1
        )

    def test_urls_uses_correct_template(self):
        """URL-адрес работает и шаблон соответствующий."""
        count = 0
        templates_url_names = {
            "/": "posts/index.html",
            f"/group/{URLTests.group.slug}/": "posts/group_list.html",
            f"/profile/{URLTests.user}/": "posts/profile.html",
            f"/posts/{URLTests.post.pk}/": "posts/post_detail.html",
            "/create/": "posts/create_post.html",
            f"/posts/{URLTests.post.pk}/edit": "posts/create_post.html",
        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = URLTests.user_auth.get(url)
                self.assertTemplateUsed(response, template)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                if count < 4:
                    count += 1
                    response = URLTests.user_random.get(url)
                    self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_URL_not_login(self):
        response = URLTests.user_random.get("/create/")
        self.assertRedirects(response, ("/auth/login/?next=/create/"))

    def test_URL_not_author(self):
        response = URLTests.user_random.get("/posts/1/edit")
        self.assertRedirects(response, ("/posts/1/"))
