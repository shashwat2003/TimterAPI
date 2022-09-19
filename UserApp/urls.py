from django.urls import path
from .views import *
urlpatterns = [
    path('', UserLoginView.as_view()),
    path('otp/', OTPView.as_view())
]
