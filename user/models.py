from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
#from .models import Content,subCategory

# class Users(AbstractUser):
#     nickname=models.CharField(max_length=30,default="test_user")
#     #email_addresss = models.CharField(max_length=32,null=True) #이메일주소
#     #user_id = models.CharField(max_length=32,default="hwid",null=True) #아이디
#     user_id = models.AutoField(primary_key=True) 
#     #password = models.CharField(max_length=16,null=True) #비밀번호

class UserCategory(models.Model):
    inserted_category=models.CharField(max_length=32)
    user_id=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    #sub_categories=models.ForeignKey(subCategory,on_delete=models.SET_NULL, null=True)
    #sub_categories=models.JSONField(default={})
    
    
class subCategory(models.Model):
    inserted_category=models.ForeignKey(UserCategory,on_delete=models.SET_NULL, null=True)
    sub_category=models.CharField(max_length=32)
    # sub_category2=models.CharField(max_length=32)
    
    # sub_category1=models.ForeignKey(Content,on_delete=models.SET_NULL, null=True)
    # sub_category2=models.ForeignKey(Content,on_delete=models.SET_NULL, null=True)
    
    #content=models.ForeignKey(Content,on_delete=models.SET_NULL, null=True)
     
    


