from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers import UserSerializer, CustomTokenObtainPairSerializer, LogoutSerializer, MyProfileSerializer, MyProfileEditSerializer, ProfileSerializer

from users.models import User
from musics.models import Review
from musics.serializers import ReviewSerializer, MusicDetailSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)
# Create your views here.

class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        user = User.objects.filter(username=request.data['username']).count()
        if user > 0:
            return Response({"message":"이미 존재"}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"가입완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)          

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class LogoutView(APIView):
    serializer = LogoutSerializer
    
    permission = (permissions.IsAuthenticated,)
    
    def post (self, request):
        
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"로그아웃 완료!"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)  
    
class FollowView(APIView):
    def post(self, request, user_id):
        you = get_object_or_404(User, id=user_id)
        me = request.user
        if me in you.follower.all():
            you.follower.remove(me)
            return Response("unfollow했습니다.", status=status.HTTP_200_OK)
        else:
            you.follower.add(me)
            return Response("follow했습니다.", status=status.HTTP_200_OK)


class ProfileView(APIView):
    def get(self, request, username):
        profile = get_object_or_404(User, username=username)
        serializer = ProfileSerializer(profile)      
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyProfileView(APIView):
    def get(self, request):
        if request.user:
            profile = get_object_or_404(User, id=request.user.id)
            serializer = MyProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("접근불가", status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        profile = get_object_or_404(User, id=request.user.id)
        serializer = MyProfileEditSerializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
