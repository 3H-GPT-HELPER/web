# Generated by Django 4.2.2 on 2023-10-02 05:02

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0002_users_nickname"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="usercategory",
            name="userCategory_id",
        ),
    ]