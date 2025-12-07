"""
Docstring for accounts.views
"""
# core import
from rest_framework import (
    generics,
)
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

# user import
from django.contrib.auth import get_user_model

# local imports
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    LoginTokenObtainSerializer,
    ChangePasswordSerializer
)

# user
User = get_user_model()

# authentication
from rest_framework_simplejwt.views import (
    TokenObtainPairView, 
    TokenRefreshSlidingView,
    TokenRefreshView
)


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
class RefreshView(TokenRefreshView):
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


"""
password changing view
"""
class ChangePasswordView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        if not user.check_password(serializer.validated_data['old_password']):
            return Response({
                'old_password': ['wrong password']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        new_password = serializer.validated_data['new_password']
        user.set_password(new_password)
        user.save()

        return Response({
            'detail': 'password updated successfully'
        }, status=status.HTTP_200_OK)