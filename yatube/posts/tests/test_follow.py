from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Post, Follow, User


class FollowerTest(TestCase):
    """Проверка функционала подписок приложения posts."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author_model = User.objects.create_user(username="author")
        cls.follower_model = User.objects.create_user(username="follower")
        cls.author = Client()
        cls.author.force_login(cls.author_model)
        cls.follower = Client()
        cls.follower.force_login(cls.follower_model)

    def test_follow_href(self):
        """Проверка создания подписки при переходе по ссылке."""
        FollowerTest.follower.get(
            reverse(
                "posts:profile_follow",
                kwargs={"username": FollowerTest.author_model.username},
            )
        )
        self.assertTrue(
            Follow.objects.filter(user=FollowerTest.follower_model).exists()
        )

    def test_follow_post(self):
        """Проверка появления поста в подписке."""
        FollowerTest.follower.get(
            reverse(
                "posts:profile_follow",
                kwargs={"username": FollowerTest.author_model.username},
            )
        )
        Post.objects.create(
            author=FollowerTest.author_model,
            text="Тестовый текст",
        )
        response = FollowerTest.follower.get(reverse("posts:follow_index"))
        object = response.context["page_obj"][0]
        self.assertEqual(object.text, "Тестовый текст")
        FollowerTest.follower.get(
            reverse(
                "posts:profile_unfollow",
                kwargs={"username": FollowerTest.author_model.username},
            )
        )
        response = FollowerTest.follower.get(reverse("posts:follow_index"))
        try:
            object = response.context["page_obj"][0]
        except IndexError:
            self.assertRaises(IndexError)
