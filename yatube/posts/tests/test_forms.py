import shutil
import tempfile

from django.test import Client, TestCase, override_settings
from django.conf import settings
from django.urls import reverse
from http import HTTPStatus
from django.core.files.uploadedfile import SimpleUploadedFile

from posts.forms import PostForm, CommentForm
from posts.models import Post, Group, Comment, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostFormTests(TestCase):
    """Проверка формы поста приложения posts."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="auth")
        cls.group = Group.objects.create(
            title="Тестовый заголовок",
            description="Тестовое описание",
            slug="test-slug",
        )
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text="Тестовый пост длиннее 15 символов",
            pk=1,
        )
        cls.form = PostForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.user_auth = Client()
        self.user_auth.force_login(PostFormTests.user)
        self.user_not_auth = Client()

    def test_create_post(self):
        """Валидная форма создает запись в post."""
        post_count = Post.objects.count()
        small_gif = (
            b"\x47\x49\x46\x38\x39\x61\x02\x00"
            b"\x01\x00\x80\x00\x00\x00\x00\x00"
            b"\xFF\xFF\xFF\x21\xF9\x04\x00\x00"
            b"\x00\x00\x00\x2C\x00\x00\x00\x00"
            b"\x02\x00\x01\x00\x00\x02\x02\x0C"
            b"\x0A\x00\x3B"
        )
        uploaded = SimpleUploadedFile(
            name="small.gif", content=small_gif, content_type="image/gif"
        )
        form_data = {
            "text": "тестовый пост, созданный в форме",
            "group": self.group.id,
            "image": uploaded,
        }
        response = self.user_auth.post(
            reverse("posts:post_create"), data=form_data, follow=True
        )
        self.assertRedirects(
            response,
            reverse(
                "posts:profile", kwargs={"username": PostFormTests.post.author}
            ),
        )
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text="тестовый пост, созданный в форме",
                group=self.group.id,
                image="posts/small.gif",
            ).exists()
        )

    def test_edit_post(self):
        """Валидная форма редактирует запись в post."""
        post_count = Post.objects.count()
        form_data = {
            "text": "тестовый пост, отредактированный в форме",
            "group": self.group.id,
        }
        response = self.user_auth.post(
            reverse(
                "posts:post_edit", kwargs={"post_id": PostFormTests.post.pk}
            ),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse(
                "posts:post_detail", kwargs={"post_id": PostFormTests.post.pk}
            ),
        )
        self.assertEqual(Post.objects.count(), post_count)
        self.assertTrue(
            Post.objects.filter(
                text="тестовый пост, отредактированный в форме",
                group=self.group.id,
                pk=1,
            ).exists()
        )

    def test_create_post_not_auth_user(self):
        """Неавторизованный клиент не может создать пост."""
        response = self.user_not_auth.get(
            reverse("posts:post_create")
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_edit_post_not_auth_user(self):
        """Неавторизованный клиент не может редактировать пост."""
        response = self.user_not_auth.get(
            reverse(
                "posts:post_edit", kwargs={"post_id": PostFormTests.post.pk}
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)


class CommentFormTests(TestCase):
    """Проверка формы комментария приложения posts."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="auth")
        cls.post = Post.objects.create(
            author=cls.user,
            text="Тестовый пост длиннее 15 символов",
            pk=1,
        )
        cls.comment = Comment.objects.create(
            author=cls.user,
            post=cls.post,
            text="Тестовый комментарий",
        )
        cls.form = CommentForm()
    
    def setUp(self):
        self.user_auth = Client()
        self.user_auth.force_login(CommentFormTests.user)
        self.user_not_auth = Client()

    def test_create_comment(self):
        """Валидная форма создает запись в comment."""
        comment_count = Comment.objects.count()
        form_data = {
            "text": "тестовый комментарий, созданный в форме",
        }
        response = self.user_auth.post(
            reverse(
                "posts:add_comment",
                kwargs={"post_id": CommentFormTests.post.pk},
            ),
            data=form_data,
            follow=True,
        )
        response_1 = self.user_auth.get(
            reverse(
                "posts:post_detail",
                kwargs={"post_id": CommentFormTests.post.pk},
            ),
        )
        self.assertRedirects(
            response,
            reverse(
                "posts:post_detail",
                kwargs={"post_id": CommentFormTests.post.pk},
            ),
        )
        self.assertEqual(Comment.objects.count(), comment_count + 1)
        self.assertTrue(
            Comment.objects.filter(
                text="тестовый комментарий, созданный в форме",
            ).exists()
        )
        self.assertEqual(
            response_1.context.get('comments').last().text,
            form_data["text"],
        )

    def test_create_comment_not_auth_user(self):
        """Неавторизованный клиент не может создать комментарий."""

        response = self.user_not_auth.get(
            reverse(
                "posts:add_comment",
                kwargs={"post_id": CommentFormTests.post.pk},
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
