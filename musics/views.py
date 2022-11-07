import random
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import get_object_or_404
from musics.models import Review,Music
from musics.serializers import ReviewSerializer,ReviewCreateSerializer,MusicSerializer,MusicCreateSerializer, MusicDetailSerializer, ReviewUpdateSerializer
from musics.recommend import recommend_musics, recommend_users, music_grades_merge, collaborative_filtering
from users.models import User
from users.serializers import RecommendUserSerializer
from django.db.models import Max 

from musics.dummy import grade_to_csv
# Create your views here.
class ReviewView(APIView):
    def post(self, request, music_id):
        request.data.update({'user': request.user.id, 'music': music_id})
        # user가 리뷰 작성 시 music_id 당 1개씩 작성 제한
        musics = Music.objects.get(id=music_id)
        reviews = musics.reviews.all()
        for review in reviews:
            if review.user==request.user:
                return Response({'message':'이미 작성 하였습니다!'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            
            # 리뷰 생성시 코사인유사도 실시간으로 측정하는 코드 추가
            grades_data = {
                'user_id':serializer.data['user'],
                'music_id':serializer.data['music'],
                'grade':serializer.data['grade'],
                'created_at':serializer.data['created_at']
            }
            grade_to_csv(grades_data) # grades_data.csv에 행 추가해줌
            collaborative_filtering(music_grades_merge())
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewDetailView(APIView):
    def put(self, request, review_id): 
        review = get_object_or_404(Review, id=review_id)
        if request.user == review.user:
            serializer = ReviewUpdateSerializer(review, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"messages": "권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)
        
    def delete(self, request, review_id): 
            review = get_object_or_404(Review, id=review_id)
            if request.user == review.user:
                review.delete()
                return Response({"messages": "삭제 되었습니다."}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"messages": "권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)


class MusicRecommandView(APIView):
    def get(self, request):
        musics = Music.objects.all()[:11]
        serializer = MusicSerializer(musics, many=True)
        
        # 메인페이지에서 추천기능 코드 추가
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

class MusicView(APIView):
    def get(self, request):
        musics = Music.objects.all().order_by("-id") # 최신순 정렬
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


class MusicRandomView(APIView):
    def get(self, request):
        # random 제한 수가 없으면 default: 20 개로 랜덤 music 목록 출력
        limit = request.data.get("limit",20)
        print(limit)
        max_id = Music.objects.aggregate(max_id=Max('id'))['max_id']
        musit_random_list = []
        while len(musit_random_list) < limit:
            random_index = random.randint(1, max_id)
            music = Music.objects.get(id=random_index)
            if music:
                serializer = MusicSerializer(music)
                musit_random_list.append(serializer.data)
        return Response(musit_random_list, status=status.HTTP_200_OK)
