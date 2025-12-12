"""
Docstring for account.urls
"""

# core imports
from django.urls import path

# local imports
from .views import(
    AllUserListView,
    RegistrationView,
    LoginView,
    PasswordChangeView
)

# jwt authentication
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('all/', AllUserListView.as_view(), name='all'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('log-in/', LoginView.as_view(), name='login'),
    path('password-change', PasswordChangeView.as_view(), name='password_change'),

    # to retrieve access token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]