"""
Docstring for users.urls
"""

# core
from django.urls import path

# local imports 
from .views import (
    RegisterView,
    LoginView,
    RefreshView,
    ProfileView,
    ChangePasswordAPIView,
)

# verify
from rest_framework_simplejwt.views import TokenVerifyView


urlpatterns = [
    path('register/', RegisterView.as_view(), name = 'register'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('refresh/', RefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('profile/<str:username>', ProfileView.as_view(), name='profile'),
    path('password/change/', ChangePasswordAPIView.as_view(), name='password_change'),
]