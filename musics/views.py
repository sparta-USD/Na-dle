from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import get_object_or_404
from musics import serializers
from musics.models import Review,Music
from musics.serializers import ReviewSerializer,ReviewCreateSerializer,MusicSerializer,MusicCreateSerializer, MusicDetailSerializer


# Create your views here.
class ReviewView(APIView):
    # def get(self, request, music_id):
    #     reviews = Review.objects.get(id=music_id)
    #     serializer = ReviewSerializer(reviews, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    
    def post(self, request, music_id):
        request.data.update({'user': request.user.id, 'music': music_id})
        serializer = ReviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewDetailView(APIView):
    def put(self, request, music_id, review_id): # music_id로 변경해야함!
        review = get_object_or_404(Review, id=review_id)
        if request.user == review.user:
            serializer = ReviewCreateSerializer(review, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)
        
    def delete(self, request, music_id, review_id): # music_id로 변경해야함!
            review = get_object_or_404(Review, id=review_id)
            if request.user == review.user:
                review.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)


class MusicView(APIView):
    def get(self, request):
        musics = Music.objects.all()
        serializer = MusicSerializer(musics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def post(self, request):
        serializer = MusicCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MusicDetailView(APIView):
    def get(self, request, music_id):
        music = get_object_or_404(Music,id=music_id)
        serializer = MusicDetailSerializer(music)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, music_id): # music_id로 변경해야함!
        music = get_object_or_404(Music, id=music_id)
        serializer = MusicCreateSerializer(music, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    def delete(self, request, music_id): # music_id로 변경해야함!
        music = get_object_or_404(Music, id=music_id)
        music.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)