from dataclasses import field
from rest_framework.serializers import ModelSerializer
from .models import *


class FollowingSerializer(ModelSerializer):

    class Meta:
        model = Following
        fields = "__all__"
