from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name", "last_name"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        if "password" in validated_data.keys():
            user.set_password(validated_data["password"])
            user.save()
        return user
