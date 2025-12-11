"""
Docstring for users.views
"""

# core imports
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

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
    permission_classes = (permissions.AllowAny,)


"""Registration"""
class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = (permissions.AllowAny,)


"""Login"""
class LoginView(TokenObtainPairView):
    serializer_class = LoginTokenObtainSerializer
    permission_classes = (permissions.AllowAny,)


"""password change"""
class PasswordChangeView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """here i am just changing the password"""
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        if not user.check_password(serializer.validated_data['old_password']):
            return Response({
                'error': 'Please enter the correct current password.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({
            'message': 'Password updated successfully.'
        }, status=status.HTTP_200_OK)
