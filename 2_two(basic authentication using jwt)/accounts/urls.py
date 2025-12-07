from .views import (
    UserListView,
    UserRegistrationView,
    LoginView,
    RefreshView,
    ProfileView,
    ChangePasswordView
)
from django.urls import path



urlpatterns = [
    path('all/', UserListView.as_view(), name = 'all_user'),
    path('registration/', UserRegistrationView.as_view(), name='register'),
    path('login/',LoginView.as_view(), name='login' ),
    path('refresh/', RefreshView.as_view(), name='refresh'),
    path('profile/<str:email>',ProfileView.as_view(), name='profile' ),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
]