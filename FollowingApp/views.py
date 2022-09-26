from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import *
from .serializers import *
# Create your views here.


class FollowingView(APIView):

    def post(self, request: Request):
        if request.user.is_authenticated and request.user.is_active:
            data = request.data if type(
                request.data) == dict else request.data.dict()
            data["follower"] = request.user.id

            if (data["user"] == request.user.id):
                return Response({"error": "Same User!"}, HTTP_400_BAD_REQUEST)

            if Following.objects.filter(user=data["user"], follower=data["follower"]).exists():
                return Response({"success": "Already Following!"})

            serailizer = FollowingSerializer(data=data)
            if serailizer.is_valid():
                serailizer.save()
                return Response({"success": "Followed Successfully!"})
            else:
                return Response({"error": serailizer.errors}, HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "User not authenticated!"}, HTTP_401_UNAUTHORIZED)
