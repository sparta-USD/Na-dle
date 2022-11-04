from rest_framework import serializers
from .models import Music
from musics.models import Review

class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = "__all__"

class MusicCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ('title','image','artist','album')



class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = Review
        fields = '__all__'


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        

class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('content', 'grade')


class MusicDetailSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)
    
    class Meta:
        model = Music
        fields = "__all__"