# Generated by Django 2.2.6 on 2022-02-13 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0004_auto_20220213_2155"),
    ]

    operations = [
        migrations.AlterField(
            model_name="group",
            name="description",
            field=models.TextField(verbose_name="описание группы"),
        ),
        migrations.AlterField(
            model_name="group",
            name="slug",
            field=models.SlugField(
                unique=True, verbose_name="Ссылка на группу"
            ),
        ),
        migrations.AlterField(
            model_name="group",
            name="title",
            field=models.CharField(
                max_length=200, verbose_name="Название группы"
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="pub_date",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="дата публикации"
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="text",
            field=models.TextField(verbose_name="текст поста"),
        ),
    ]
