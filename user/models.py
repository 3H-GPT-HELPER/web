from django.db import models


# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=30,default="hw")
    email_address = models.CharField(max_length=32) #이메일주소
    user_id = models.CharField(max_length=16,default="hwid",null=True) #아이디
    password = models.CharField(max_length=16,null=True) #비밀번호
    #google social login시 수정

class UserKeywords(models.Model):
    userKeywords_id=models.IntegerField()
    name=models.CharField(max_length=20)
    user_id=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)



