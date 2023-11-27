from django.db import models
from user.models import UserCategory
from django.contrib.auth.models import User


# Create your models here.
class Content(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    question=models.TextField(default="")
    answer=models.TextField()
    topics=models.TextField(default="",null=True)

    inserted_category=models.ForeignKey(UserCategory,on_delete=models.SET_NULL, null=True)
    sub_category1=models.CharField(max_length=32,null=True)
    sub_category2=models.CharField(max_length=32,null=True)
