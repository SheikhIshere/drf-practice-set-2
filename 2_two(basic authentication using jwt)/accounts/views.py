"""
Docstring for accounts.views
"""
# core import
from rest_framework import (
    generics,
)
from rest_framework import permissions

# user import
from django.contrib.auth import get_user_model

# local imports
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    LoginTokenObtainSerializer
)

# user
User = get_user_model()

# authentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshSlidingView


"""
user list show
"""
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


"""
user registration login
"""
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny, )


"""
login
"""
class LoginView(TokenObtainPairView):
    """
    jwt LoginView
    """
    serializer_class = LoginTokenObtainSerializer
    permission_classes = (permissions.AllowAny, )


"""
Token refresh view
"""
class RefreshView(TokenRefreshSlidingView):
    """to get access token using refresh token"""
    permission_classes = (permissions.AllowAny, )


"""
single profile retrieve view
"""
class ProfileView(generics.RetrieveAPIView):
    """here i am providing single user detail for it's profile"""
    queryset = User.objects.all()
    serializer_class = UserSerializer # for now using the general in big project i will be using more specified serializer\
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'email'