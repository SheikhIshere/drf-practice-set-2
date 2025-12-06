from .views import (
    UserListView,
    UserRegistrationView,
    LoginView,
    RefreshView,
    ProfileView
)
from django.urls import path



urlpatterns = [
    path('all/', UserListView.as_view(), name = 'all_user'),
    path('registration/', UserRegistrationView.as_view(), name='register'),
    path('login/',LoginView.as_view(), name='login' ),
    path('refresh/', RefreshView.as_view(), name='refresh'),
    path('profile/<str:username>',ProfileView.as_view(), name='profile' )
]