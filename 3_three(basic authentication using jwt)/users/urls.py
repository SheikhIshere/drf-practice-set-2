"""
Docstring for users.urls
"""
# core imports
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


# local imports
from .views import(
    UserListView,
    RegistrationView,
    LoginView,
    PasswordChangeView,
)

urlpatterns = [
    path('users/all/', UserListView.as_view(), name='user_list'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),


    # token verification
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    
]