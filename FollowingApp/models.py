from django.db import models

# Create your models here.


class Following(models.Model):
    follower = models.ForeignKey(
        "UserApp.User", on_delete=models.CASCADE, related_name="followings")
    user = models.ForeignKey(
        "UserApp.User", on_delete=models.CASCADE, related_name="followers")
    timestamp = models.DateTimeField(auto_now_add=True)
