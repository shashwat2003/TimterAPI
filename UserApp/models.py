import email
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    verification_status = models.BooleanField(default=False)
    role = models.ForeignKey(
        'Role', on_delete=models.SET_NULL, default=2, null=True)


class Role(models.Model):
    name = models.CharField(max_length=200)


class OTP(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=200)
    otp = models.IntegerField(primary_key=True)
    expiry = models.DateTimeField()
