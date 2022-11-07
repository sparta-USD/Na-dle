from rest_framework import serializers
from .models import Music
from musics.models import Review

class MusicSerializer(serializers.ModelSerializer):
    avg_grade = serializers.SerializerMethodField()
    
    class Meta:
        model = Music
        fields = "__all__"
    
    def get_avg_grade(self, obj):
        return obj.avg_grade()

class MusicCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ('title','image','artist','album')

class MusicSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ('title','image','artist')

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    music = MusicSimpleSerializer()
    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = Review
        fields = '__all__'


class ReviewCreateSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    def get_user(self, obj):
        return obj.user.username
    
    def get_user_id(self, obj):
        return obj.user.id

    class Meta:
        model = Review
        fields = '__all__'


                

class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('content', 'grade')


class MusicDetailSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)
    avg_grade = serializers.SerializerMethodField()
    
    class Meta:
        model = Music
        fields = "__all__"
        
    def get_avg_grade(self, obj):
        return obj.avg_grade()
