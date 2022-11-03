from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import get_object_or_404
from musics import serializers
from musics.models import Review
from musics.serializers import ReviewSerializer,ReviewCreateSerializer
from django.contrib.auth.decorators import login_required

# Create your views here.
class ReviewView(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def post(self, request):
        print(request.user)
        serializer = ReviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewDetailView(APIView):
    def put(self, request, id): # music_id로 변경해야함!
        review = get_object_or_404(Review, id=id)
        if request.user == review.user:
            serializer = ReviewCreateSerializer(review, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)
        
    def delete(self, request, id): # music_id로 변경해야함!
            review = get_object_or_404(Review, id=id)
            if request.user == review.user:
                review.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)