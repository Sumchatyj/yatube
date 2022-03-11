import shutil
import tempfile

from django.core.cache import cache
from django.conf import settings
from django import forms
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from datetime import datetime
from django.core.files.uploadedfile import SimpleUploadedFile

from posts.models import Post, Group, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
SMALL_GIF = (
    b"\x47\x49\x46\x38\x39\x61\x02\x00"
    b"\x01\x00\x80\x00\x00\x00\x00\x00"
    b"\xFF\xFF\xFF\x21\xF9\x04\x00\x00"
    b"\x00\x00\x00\x2C\x00\x00\x00\x00"
    b"\x02\x00\x01\x00\x00\x02\x02\x0C"
    b"\x0A\x00\x3B"
)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsPagesTest(TestCase):
    """Проверка страниц приложения posts."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="auth")
        cls.user_auth = Client()
        cls.user_auth.force_login(cls.user)
        cls.uploaded = SimpleUploadedFile(
            name="small.gif", content=SMALL_GIF, content_type="image/gif"
        )
        cls.group = Group.objects.create(
            title="Тестовый заголовок",
            description="Тестовое описание",
            slug="test-slug",
        )
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text="Тестовый пост длиннее 15 символов",
            pub_date=datetime.now(),
            image="posts/small.gif",
            pk=1,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_pages_uses_correct_template(self):
        """URL-адрес по имени использует соответствующий шаблон."""
        templates_pages_names = {
            reverse("posts:index"): "posts/index.html",
            reverse(
                "posts:group_posts", kwargs={"slug": PostsPagesTest.group.slug}
            ): "posts/group_list.html",
            reverse(
                "posts:profile", kwargs={"username": PostsPagesTest.user}
            ): "posts/profile.html",
            reverse(
                "posts:post_detail", kwargs={"post_id": PostsPagesTest.post.pk}
            ): "posts/post_detail.html",
            reverse("posts:post_create"): "posts/create_post.html",
            reverse(
                "posts:post_edit", kwargs={"post_id": PostsPagesTest.post.pk}
            ): "posts/create_post.html",
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = PostsPagesTest.user_auth.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = PostsPagesTest.user_auth.get(reverse("posts:index"))
        first_object = response.context["page_obj"][0]
        first_object_params = {
            first_object.text: PostsPagesTest.post.text,
            first_object.pub_date: PostsPagesTest.post.pub_date,
            first_object.author: PostsPagesTest.post.author,
            first_object.group: PostsPagesTest.post.group,
            first_object.image: PostsPagesTest.post.image,
        }
        for param1, param2 in first_object_params.items():
            with self.subTest(param=param1):
                self.assertEqual(param1, param2)

    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = PostsPagesTest.user_auth.get(
            reverse(
                "posts:group_posts", kwargs={"slug": PostsPagesTest.group.slug}
            )
        )
        first_object = response.context["page_obj"][0]
        first_object_params = {
            first_object.text: PostsPagesTest.post.text,
            first_object.pub_date: PostsPagesTest.post.pub_date,
            first_object.author: PostsPagesTest.post.author,
            first_object.group: PostsPagesTest.post.group,
            first_object.image: PostsPagesTest.post.image,
        }
        for param1, param2 in first_object_params.items():
            with self.subTest(param=param1):
                self.assertEqual(param1, param2)
        second_object = response.context["group"]
        self.assertEqual(
            second_object,
            PostsPagesTest.post.group,
        )

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = PostsPagesTest.user_auth.get(
            reverse("posts:profile", kwargs={"username": PostsPagesTest.user})
        )
        first_object = response.context["page_obj"][0]
        first_object_params = {
            first_object.text: PostsPagesTest.post.text,
            first_object.pub_date: PostsPagesTest.post.pub_date,
            first_object.author: PostsPagesTest.post.author,
            first_object.group: PostsPagesTest.post.group,
            first_object.image: PostsPagesTest.post.image,
        }
        for param1, param2 in first_object_params.items():
            with self.subTest(param=param1):
                self.assertEqual(param1, param2)
        second_object = response.context["post_count"]
        self.assertEqual(second_object, 1)
        third_object = response.context["author"]
        self.assertEqual(
            third_object,
            PostsPagesTest.post.author,
        )

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = PostsPagesTest.user_auth.get(
            reverse(
                "posts:post_detail", kwargs={"post_id": PostsPagesTest.post.pk}
            )
        )
        first_object = response.context["post"]
        first_object_params = {
            first_object.text: PostsPagesTest.post.text,
            first_object.pub_date: PostsPagesTest.post.pub_date,
            first_object.author: PostsPagesTest.post.author,
            first_object.group: PostsPagesTest.post.group,
            first_object.image: PostsPagesTest.post.image,
        }
        for param1, param2 in first_object_params.items():
            with self.subTest(param=param1):
                self.assertEqual(param1, param2)
        second_object = response.context["post_count"]
        self.assertEqual(second_object, 1)

    def test_post_create_page_show_correct_context(self):
        """Шаблон post_create_ сформирован с правильным контекстом."""
        response = PostsPagesTest.user_auth.get(reverse("posts:post_create"))
        form_fields = {
            "text": forms.fields.CharField,
            "group": forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get("form").fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_edit_page_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = PostsPagesTest.user_auth.get(
            reverse(
                "posts:post_edit", kwargs={"post_id": PostsPagesTest.post.pk}
            )
        )
        form_fields = {
            "text": forms.fields.CharField,
            "group": forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get("form").fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_has_only_one_group(self):
        """У поста только одна группа."""
        self.assertEqual(
            str(Group.objects.filter(posts=1)),
            "<QuerySet [<Group: Тестовый заголовок>]>",
        )

    def test_cache_for_index(self):
        """У index работает кэш."""
        response_1 = PostsPagesTest.user_auth.get(reverse("posts:index"))
        Post.objects.get(pk=1).delete()
        response_2 = PostsPagesTest.user_auth.get(reverse("posts:index"))
        self.assertEqual(response_1.content, response_2.content)
        cache.clear()
        response_2 = PostsPagesTest.user_auth.get(reverse("posts:index"))
        self.assertNotEqual(response_1.content, response_2.content)
