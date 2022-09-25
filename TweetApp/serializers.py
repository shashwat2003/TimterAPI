from .models import *
from rest_framework.serializers import ModelSerializer, ImageField, ListField, IntegerField
# from rest_framework import serializers
from UserApp.serializers import TweetedUserSerializer


class TweetSerializer(ModelSerializer):
    class Meta:
        model = Tweet
        fields = ["user", "text", "timestamp", "parent_tweet"]


class TweetViewSerializer(ModelSerializer):
    user = TweetedUserSerializer(read_only=True)

    def __init__(self, instance=None, data=..., **kwargs):
        self.requested_id = kwargs.pop("user")
        super().__init__(instance, data, **kwargs)

    class Meta:
        model = Tweet
        fields = ["user", "text", "timestamp", "id"]
        depth = 1

    def get_media(self, instance):
        return [tweet.media.url for tweet in TweetMedia.objects.filter(tweet=instance.id)]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["media"] = self.get_media(instance)
        data["liked"] = True if instance.likes.filter(
            id=self.requested_id).exists() else False
        data["retweeted"] = True if instance.retweets.filter(
            id=self.requested_id).exists() else False
        # retweeted_by
        # data["is_retweeted"] = instance
        return data


class TweetMediaSerializer(ModelSerializer):
    class Meta:
        model = TweetMedia
        fields = "__all__"
