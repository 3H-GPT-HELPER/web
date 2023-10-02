from django.db import models
from user.models import UserCategory,Users


# Create your models here.
class Content(models.Model):
    user_id=models.ForeignKey(Users,on_delete=models.SET_NULL,null=True)
    answer=models.TextField()
    topics=models.TextField(default="",null=True)

    inserted_category=models.ForeignKey(UserCategory,on_delete=models.SET_NULL, null=True)
    #selected_category=models.CharField(max_length=32,null=True)
    
