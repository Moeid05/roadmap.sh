from django.urls import path
from django.conf import settings 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserRegistrationView
auth_method = settings.AUTHENTICATION
urlpatterns = [
    path('register/', UserRegistrationView.as_view() ),


]
urlpatterns += [
            path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
            path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
            ] if auth_method == 'jwt' else [path('login/', obtain_auth_token, name='api_token_auth')]
