<<<<<<< HEAD
# Generated by Django 4.2.2 on 2023-11-20 05:46
=======
# Generated by Django 4.2.4 on 2023-11-22 07:23
>>>>>>> main

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Content",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("question", models.TextField(default="")),
                ("answer", models.TextField()),
                ("topics", models.TextField(default="", null=True)),
                ("sub_category1", models.CharField(max_length=32, null=True)),
                ("sub_category2", models.CharField(max_length=32, null=True)),
                (
                    "inserted_category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="user.usercategory",
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
