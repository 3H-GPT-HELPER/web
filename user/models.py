from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname=models.CharField(max_length=30,default="test_user")
    email_addresss = models.CharField(max_length=32,null=True) #이메일주소
    user_id = models.CharField(max_length=32,default="hwid",null=True) #아이디
    password = models.CharField(max_length=16,null=True) #비밀번호
    
    
class UserCategory(models.Model):
    userCategory_id=models.IntegerField()
    inserted_category=models.CharField(max_length=32)
    user_id=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)



