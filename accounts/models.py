from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Role(models.Model):
    role_name = models.CharField(max_length = 30, unique = True)
    def __str__(self):
        return self.role_name




class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete = models.SET_NULL, null = True, blank = True)

from django.contrib.auth.hashers import make_password
from django.db.utils import OperationalError


def create_default_admin():
    try:
        if not User.objects.filter(username="admin").exists():
            role, created = Role.objects.get_or_create(role_name="Admin")

            User.objects.create(
                username="admin",
                password=make_password("password"),
                role=role,
                is_staff=True,
                is_superuser=True,
                is_active=True
            )
            print("Default admin user created")

    except OperationalError:
        pass