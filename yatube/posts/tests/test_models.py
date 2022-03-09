from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post


User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="auth")
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="Тестовый слаг",
            description="Тестовое описание",
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text="Тестовый пост длиннее 15 символов",
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post = PostModelTest.post
        group = PostModelTest.group
        values = (
            (str(post), PostModelTest.post.text[:15]),
            (str(group), PostModelTest.group.title),
        )
        for field, expected_value in values:
            with self.subTest(field=field):
                self.assertEqual(
                    field, expected_value, "Ошибка в методе __str__ модели"
                )

    def test_models_have_verbose_names(self):
        """Проверяем, что у моделей прописаны правильные verbose names"""
        post = PostModelTest.post
        group = PostModelTest.group
        field_verboses_group = {
            "title": "Название группы",
            "slug": "Ссылка на группу",
            "description": "Описание группы",
        }
        field_verboses_post = {
            "text": "Текст поста",
            "pub_date": "Дата создания",
            "author": "Автор",
            "group": "Группа",
        }
        for field, expected_value in field_verboses_group.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).verbose_name,
                    expected_value,
                    "Ошибка в verbose name модели Group",
                )
        for field, expected_value in field_verboses_post.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name,
                    expected_value,
                    "Ошибка в verbose name модели Post",
                )
