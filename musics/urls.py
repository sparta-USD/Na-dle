from django.urls import path
from musics import views

urlpatterns = [
    path('reviews/', views.ReviewView.as_view(), name='review_view'),#music_id 추가필요
    path('reviews/put/<int:id>/', views.ReviewDetailView.as_view(), name='review_detail_view'),#music_id 추가필요
    
]
