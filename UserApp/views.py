from datetime import datetime, timedelta
from random import randint

from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from TimterAPI.constants import yag
from django.core.files.storage import default_storage


from .models import *
from .serializers import *

# Create your views here


def generate_otp_content(otp):
    return '''
OTP for your Timter Registration is {0}. 
To create an account, please verify your email address by entering the code. Verification code expires in 30 minutes.
Code expired? Try registering again to receive a new code. If you did not request this code, please ignore this. TIMTER ID cannot be created.
Please do not reply directly to this email. This is an autogenerated email.

© 2021 Timter, Inc. All rights reserved
'''.format(otp)


class UserLoginView(APIView):
    def get(self, request: Request):
        if request.user.is_authenticated and request.user.is_active:
            return Response({"verified": True})
        else:
            return Response({"verified": False})

    def post(self, request: Request):
        print(request.data.keys())
        if "email" in request.data.keys():
            user = User.objects.filter(
                email=request.data.get("email").strip()).first()
            if user is None:
                return Response({"error": "User Not Found!"}, status=HTTP_400_BAD_REQUEST)

        else:
            username = request.data.get("username")
            print(username)
        user = authenticate(username=username,
                            password=request.data.get("password"))
        if user is not None:
            isFirstLogin = True if user.last_login == None else False
            login(request, user)
            return Response({"success": "Login Success!", "isFirstLogin": isFirstLogin})
        else:
            return Response({"error": "User Not Found!"}, status=HTTP_400_BAD_REQUEST)


class UserRegistrationView(APIView):
    def post(self, request: Request):
        otp = eval(request.data.get("otp", "-1"))
        email = request.data.get("email", "").strip()
        if otp != -1 and email != "" and OTP.objects.filter(otp=otp, expiry__gt=datetime.now(), email=email).exists():
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                OTP.objects.get(otp=otp, email=email).delete()
                return Response({"success": "Account Creation Successful!"})
            else:
                return Response({"error": serializer.errors}, HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "OTP is Incorrect!"}, HTTP_400_BAD_REQUEST)

    def put(self, request: Request):
        if request.user.is_authenticated and request.user.is_active:
            data = request.data if type(
                request.data) == dict else request.data.dict()
            data.pop("username", "")
            data.pop("email", "")
            data.pop("verification_status", "")
            data.pop("special_status", "")

            serializer = UserSerializer(
                instance=request.user, data=data, partial=True)
            if serializer.is_valid():
                if request.user.profile_photo is not None:
                    try:
                        print(request.user.profile_photo.path)
                        default_storage.delete(request.user.profile_photo.path)
                    except:
                        pass
                serializer.save()
                return Response({"success": "Updated Successfully!"})
            else:
                return Response({"error": serializer.errors}, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "User Not Authenticated!"}, status=HTTP_401_UNAUTHORIZED)


class OTPView(APIView):
    def post(self, request: Request):
        email = request.data.get("email", "").strip()
        username = request.data.get("username", "").strip()
        if email == "" or username == "":
            return Response({"error": "Email or UserName cannot be null!"}, status=HTTP_400_BAD_REQUEST)
        if not User.objects.filter(Q(username=username) | Q(email=email)).exists() and not OTP.objects.filter(Q(email=email) | Q(username=username)).filter(expiry__gt=datetime.now()).exists():
            if OTP.objects.filter(Q(email=email) | Q(username=username)).first() is not None:
                try:
                    OTP.objects.get(email=email).delete()
                except:
                    pass

                try:
                    OTP.objects.get(username=username).delete()
                except:
                    pass

            otp = OTP.objects.create(email=email, otp=randint(
                100000, 999999), expiry=datetime.now()+timedelta(minutes=30), username=username)
            yag.send(to=email, subject='[OTP] Registration OTP for Timter!',
                     contents=generate_otp_content(otp.otp))
            return Response({"success": "OTP have been sent to your mail address!"})
        else:
            return Response({"error": "Either the OTP is already generated or the email or username already exists with us!"}, status=HTTP_400_BAD_REQUEST)
