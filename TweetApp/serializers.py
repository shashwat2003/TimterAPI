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
        self.following = kwargs.pop("following", [])
        self.Meta.depth = kwargs.pop("depth", 1)
        print(self.Meta.depth)
        super().__init__(instance, data, **kwargs)

    class Meta:
        model = Tweet
        fields = ["user", "text", "timestamp", "id", "parent_tweet"]

    def get_media(self, instance):
        return [tweet.media.url for tweet in TweetMedia.objects.filter(tweet=instance.id)]

    def to_representation(self, instance):
        if instance.parent_tweet is not None and self.Meta.depth > 0:
            self.fields['parent_tweet'] = TweetViewSerializer(
                read_only=True, user=instance.parent_tweet.user.id, depth=0)
        data = super().to_representation(instance)
        data["media"] = self.get_media(instance)
        data["liked"] = True if instance.likes.filter(
            id=self.requested_id).exists() else False
        data["retweeted"] = True if instance.retweets.filter(
            id=self.requested_id).exists() else False
        data["retweets"] = instance.retweets.count()
        data["likes"] = instance.likes.count()
        data["retweeted_by"] = instance.retweets.filter(
            id__in=self.following).values_list("username", flat=True)
        return data


class TweetMediaSerializer(ModelSerializer):
    class Meta:
        model = TweetMedia
        fields = "__all__"
