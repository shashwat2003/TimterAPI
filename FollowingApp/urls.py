from django.urls import path
from .views import *
urlpatterns = [
    path('', FollowingView.as_view())
]
