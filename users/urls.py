from django.urls import path
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)

urlpatterns = [
    path('signup/', views.UserView.as_view(), name='user_view'),
    path('signin/', views.SigninView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('follow/<int:user_id>/', views.FollowView.as_view(), name='follow_view'),
    path('profile/', views.MyProfileView.as_view(), name='my_profile'),
    path('<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('first/<int:user_id>/', views.FirstUserView.as_view(), name='first'),
]
