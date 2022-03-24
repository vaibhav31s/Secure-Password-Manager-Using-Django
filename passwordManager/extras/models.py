from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Passwords(models.Model):
    user = models.ForeignKey(User,verbose_name="",on_delete=models.CASCADE)
    name =  models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email  = models.CharField(max_length=100)
    logo = models.CharField(max_length=100)
    


    def __str__(self):
        return self.name
    class Meta:
        ordering = ["-id"]
