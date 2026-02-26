from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Role(models.Model):
    role_name = models.CharField(max_length = 30, unique = True)
    def __str__(self):
        return self.role_name




class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete = models.SET_NULL, null = True, blank = True, related_name = 'users')