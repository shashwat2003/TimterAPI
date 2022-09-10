from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    verification_status = models.BooleanField(default=False)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL)


class Role(models.Model):
    name = models.CharField(max_length=200)
