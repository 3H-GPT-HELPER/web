from django.db import models
from user.models import UserKeywords

# Create your models here.
class Content(models.Model):
    userName=models.CharField(max_length=20,default="hw")
    answer=models.TextField()
    topics=models.TextField(default="")

    category=models.CharField(max_length=20,default="")
    
