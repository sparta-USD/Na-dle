from rest_framework import serializers
from users.models import User
from musics.serializers import ReviewSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=['username', 'fullname', 'password']
        
    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user
     
    def update(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user


# 221104 최해민 추천유저시리얼라이저 추가
class RecommendUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'fullname', 'profile_image']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token
    
    
class LogoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['refresh',]
        
    refresh = serializers.CharField()
    
    default_error_messages = {
        'bad_token': ('토큰이 만료됐거나 유효하지않습니다.')
    }
    
    def validate(self,attrs):
        self.token =attrs['refresh']
        return attrs
    
    def save(self, **kwargs):
        
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')

class ProfileSerializer(serializers.ModelSerializer):
    my_reviews = ReviewSerializer(many=True)
    
    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = User
        fields = "__all__"
        
class ProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=("profile_image", "fullname", "email")
        
