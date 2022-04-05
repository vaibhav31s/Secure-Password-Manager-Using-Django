from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, User
# Create your models here.
class Passwords(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="",on_delete=models.CASCADE)
    name =  models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email  = models.CharField(max_length=100)
    logo = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ["-id"]

class newUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="",on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15)
    
    class Meta:
        ordering = ["-id"]
    

