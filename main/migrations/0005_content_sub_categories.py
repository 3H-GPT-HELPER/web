# Generated by Django 4.2.2 on 2023-11-12 03:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0004_content_question"),
    ]

    operations = [
        migrations.AddField(
            model_name="content",
            name="sub_categories",
            field=models.JSONField(default={}),
        ),
    ]
