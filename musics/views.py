from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import get_object_or_404
from musics.models import Review,Music
from musics.serializers import ReviewSerializer,ReviewCreateSerializer,MusicSerializer,MusicCreateSerializer, MusicDetailSerializer, ReviewUpdateSerializer
from musics.recommend import recommend_musics, recommend_users
from users.models import User
from users.serializers import RecommendUserSerializer

# Create your views here.
class ReviewView(APIView):
    def post(self, request, music_id):
        request.data.update({'user': request.user.id, 'music': music_id})
        serializer = ReviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewDetailView(APIView):
    def put(self, request, music_id, review_id): 
        review = get_object_or_404(Review, id=review_id)
        if request.user == review.user:
            serializer = ReviewUpdateSerializer(review, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)
        
    def delete(self, request, music_id, review_id): 
            review = get_object_or_404(Review, id=review_id)
            if request.user == review.user:
                review.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)


class MusicView(APIView):
    def get(self, request):
        musics = Music.objects.all()[:11]
        serializer = MusicSerializer(musics, many=True)
        
        recommend_users_id = recommend_users(request.user.id)
        recommend_musics_id = recommend_musics(request.user.id)
        
        re_users = User.objects.filter(id__in=recommend_users_id)
        re_musics = Music.objects.filter(id__in=recommend_musics_id)
        
        re_musics_serializer = MusicSerializer(re_musics, many=True)
        re_users_serializer = RecommendUserSerializer(re_users, many=True)
        
        context = {
            "musics" : serializer.data,
            "recommend_users" : re_users_serializer.data,
            "recommend_musics" : re_musics_serializer.data
        }
        return Response(context, status=status.HTTP_200_OK)

    
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

    def put(self, request, music_id): 
        music = get_object_or_404(Music, id=music_id)
        serializer = MusicCreateSerializer(music, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    def delete(self, request, music_id): 
        music = get_object_or_404(Music, id=music_id)
        music.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)