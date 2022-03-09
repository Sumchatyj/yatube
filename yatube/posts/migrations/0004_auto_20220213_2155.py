# Generated by Django 2.2.6 on 2022-02-13 21:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0003_auto_20220122_2117"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="post",
            options={"ordering": ["-pub_date"]},
        ),
        migrations.AlterField(
            model_name="group",
            name="description",
            field=models.TextField(verbose_name="group`s description"),
        ),
        migrations.AlterField(
            model_name="group",
            name="slug",
            field=models.SlugField(unique=True, verbose_name="group`s link"),
        ),
        migrations.AlterField(
            model_name="group",
            name="title",
            field=models.CharField(
                max_length=200, verbose_name="group`s title"
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Автор",
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="posts",
                to="posts.Group",
                verbose_name="Группа",
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="pub_date",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="publication date"
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="text",
            field=models.TextField(verbose_name="post`s text"),
        ),
    ]