from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import UniqueConstraint

from core.models import CreatedModel


User = get_user_model()


class Group(models.Model):
    title = models.CharField("Название группы", max_length=200)
    slug = models.SlugField("Ссылка на группу", unique=True)
    description = models.TextField("Описание группы")

    def __str__(self) -> str:
        return self.title


class Post(CreatedModel):
    text = models.TextField("Текст поста")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="posts",
        verbose_name="Группа",
    )
    image = models.ImageField("Картинка", upload_to="posts/", blank=True)

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self) -> str:
        return self.text[:15]


class Comment(CreatedModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name="Комментарий",
        related_name="comments",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )
    text = models.TextField("Текст комментария")


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Подписчик",
        related_name="follower",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name="following",
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=["author", "user"], name="unique_follower")
        ]
