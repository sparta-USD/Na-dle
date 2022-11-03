from django.urls import path
from musics import views

urlpatterns = [
    path('reviews/<int:music_id>/', views.ReviewView.as_view(), name='review_view'),#music_id 추가필요
    path('reviews/<int:music_id>/<int:review_id>/', views.ReviewDetailView.as_view(), name='review_detail_view'),#music_id 추가필요
    path('', views.MusicView.as_view(), name='music_view'),
    path('<int:music_id>/', views.MusicDetailView.as_view(), name='music_detail_view'),#music_id 추가필요
]
