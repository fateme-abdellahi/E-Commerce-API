from django.urls import path
from user import views
from user.views import ProfileApiView
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,TokenVerifyView)


urlpatterns = [
    path('api/accounts/register', views.RegisterAPIView.as_view(), name='register'),
    path('api/accounts/login', views.LoginAPIView.as_view(), name='login'),
    path('api/accounts/logout', views.LogoutAPIView.as_view(), name='logout'),
    path('api/profile/<user_id>', ProfileApiView.as_view(), name='profile'),


    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]

