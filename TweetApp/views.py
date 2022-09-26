from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from UserApp.models import User
from .serializers import *
from django.core.files.storage import default_storage

# Create your views here.


class TweetView(APIView, PageNumberPagination):
    page_size = 2

    def get(self, request: Request):
        following = list(request.user.followings.all(
        ).values_list("user_id", flat=True))
        tweets = Tweet.objects.filter(
            user__in=following).order_by("-timestamp")
        retweets = Tweet.objects.filter(
            retweets__in=following, parent_tweet=None)
        tweets = tweets.union(retweets).order_by("-timestamp")
        serializer = TweetViewSerializer(
            self.paginate_queryset(tweets, request, view=self), many=True, user=request.user.id, following=following)
        return self.get_paginated_response(serializer.data)

    def post(self, request: Request):
        if request.user.is_authenticated and request.user.is_active:
            data = request.data if type(
                request.data) == dict else request.data.dict()
            data["user"] = request.user.id
            serializer = TweetSerializer(data=data)
            if serializer.is_valid():
                tweet = serializer.save()
                media = [{"tweet": tweet.id, "media": file}
                         for file in request.FILES.getlist("file")]
                serializer = TweetMediaSerializer(data=media, many=True)
                serializer.is_valid()
                serializer.save()
                return Response({"success": "Tweeted!"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors)
        else:
            return Response({"error": "User Not Authenticated!"}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request: Request):
        if request.user.is_authenticated and request.user.is_active:
            tweet = Tweet.objects.filter(id=request.data.get("id")).first()
            if tweet is not None:
                if tweet.user == request.user:
                    for file in TweetMedia.objects.filter(tweet=tweet):
                        try:
                            default_storage.delete(file.media.path)
                        except:
                            pass
                        file.delete()
                    tweet.delete()
                    return Response({"success": "Tweet Deleted Successfully!"})
                else:
                    return Response({"error": "Not your Tweet!"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"error": "Tweet not found!"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "User Not Authenticated!"}, status=status.HTTP_401_UNAUTHORIZED)
