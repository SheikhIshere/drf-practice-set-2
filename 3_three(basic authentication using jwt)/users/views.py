"""
Docstring for users.views
"""

# core imports
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

# authentication
from rest_framework_simplejwt.views import TokenObtainPairView

# local imports
from .serializers import(
    UserListSerializer, 
    RegistrationSerializer,
    LoginTokenObtainSerializer,
    ChangePasswordSerializer
)

# user model
from django.contrib.auth import get_user_model
User = get_user_model()


# main codes

"""user list"""
class UserListView(generics.ListAPIView):
    """here i am just providing the list of all user"""
    queryset = User.objects.all()
    serializer_class = UserListSerializer


"""Registration"""
class RegistrationView(APIView):
    serializer_class = RegistrationSerializer