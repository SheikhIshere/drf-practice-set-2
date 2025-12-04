"""
Docstring for users.views
"""


# core imports
from rest_framework import (
    generics, 
    permissions, 
    status
)
from rest_framework.response import Response
from rest_framework.views import APIView

# user model
from django.contrib.auth import get_user_model

# authentication
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from rest_framework_simplejwt.tokens import RefreshToken

# local imports
from .serializers import (
    UserSerializer,
    RegistrationSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer
)


# user
User = get_user_model()


"""
registrations view
"""
class RegisterView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = (permissions.AllowAny, )


"""
login view
"""
class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = (permissions.AllowAny, )

"""
refresh view
"""
class RefreshView(TokenRefreshView):
    permission_classes = (permissions.AllowAny, )


"""
provide all of the user profile
"""
class ProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny, )
    lookup_field = 'username'



"""
for changing password
"""
class ChangePasswordAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        if not user.check_password(serializer.validated_data['old_password']):
            return Response({
                'old_password': ['Wrong password']
            }, status=status.HTTP_400_BAD_REQUEST
            )
    
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({
            'detail': 'password updated successfully'
        }, status=status.HTTP_200_OK
        )