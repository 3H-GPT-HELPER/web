from django.db import models

# Create your models here.
class Content(models.Model):
    userName=models.CharField(max_length=20,default="hw")
    answer=models.TextField()
    keywords=models.TextField(default="")
    
