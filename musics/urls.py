from django.urls import path
from musics import views

urlpatterns = [
    path('reviews/', views.ReviewView.as_view(), name='review_view'),#music_id 추가필요
]
