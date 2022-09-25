from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name", "last_name",
                  "verification_status", "profile_photo", "special_status", "bio", "website"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        if "password" in validated_data.keys():
            user.set_password(validated_data["password"])
            user.save()
        return user


class TweetedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name",
                  "verification_status", "profile_photo", "special_status"]
        extra_kwargs = {
            'password': {'write_only': True}
        }
