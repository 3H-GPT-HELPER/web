# Generated by Django 4.2.2 on 2023-06-18 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="content",
            name="userName",
            field=models.CharField(default="hw", max_length=20),
        ),
    ]
