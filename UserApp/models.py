import email
from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

def upload_path(instance, filename):
    return "users/{0}".format(filename)

class User(AbstractUser):
    verification_status = models.BooleanField(default=False)
    role = models.ForeignKey(
        'Role', on_delete=models.SET_NULL, default=2, null=True)
    bio = models.TextField(null=True, default=None)
    profile_photo = models.ImageField(null=True, default=None, upload_to=upload_path)
    website = models.URLField(null=True, default=None)
    special_status = models.TextField(null=True, default=None)


class Role(models.Model):
    name = models.CharField(max_length=200)


class OTP(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=200)
    otp = models.IntegerField(primary_key=True)
    expiry = models.DateTimeField()
