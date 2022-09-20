from django.db import models

# Create your models here.


def upload_media_path(instance, filename):
    return "tweet_{0}/{1}".format(instance.tweet.id, filename)


class Tweet(models.Model):
    user = models.ForeignKey("UserApp.User", on_delete=models.CASCADE)
    tweet = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField("UserApp.User", related_name="liked_tweets")
    retweets = models.ManyToManyField(
        "UserApp.User", related_name="retweeted_tweets")


class TweetMedia(models.Model):
    tweet = models.ForeignKey(
        Tweet, on_delete=models.SET_DEFAULT, default=0)
    media = models.FileField(upload_to=upload_media_path)
