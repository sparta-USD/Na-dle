from rest_framework import serializers
from .models import Music
from musics.models import Review

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = "__all__"


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
        fields = ("content","grade")

