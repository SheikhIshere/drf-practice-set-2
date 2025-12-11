"""
Docstring for account.views
"""

# core imports
from rest_framework import (
    generics, 
    status, 
    permissions,
    views,
)
from rest_framework.response import Response

# user import 
from django.contrib.auth import get_user_model
User = get_user_model()

# local imports
from .serializers import(
    AllUserSerializer,
    RegistrationSerializer,
    LoginSerializer,
    PasswordChangeSerializer
)

# jwt imports
from rest_framework_simplejwt.views import TokenObtainPairView


"""showing list of all user for no reason"""
class AllUserListView(generics.ListAPIView):
    serializer_class = AllUserSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()


"""Registration though all done in serializer"""
class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = (permissions.AllowAny,)


"""Login"""
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny)


"""password change"""
class PasswordChangeView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        """
        here i am writing the spell to change password
        yoo!! widget
        """

        # first i am initializing the serializer
        serializer = PasswordChangeSerializer(data=request.data,  context={'request': request})
        serializer.is_valid(raise_exception=True)

        # then i am defining wo is the user
        user = request.user

        # change the password using set_password
        user.set_password(serializer.validated_data['new_password'])
        user.save() # saving the updated user model

        return Response({
            'success':'password updated successfully'
        }, status=status.HTTP_200_OK)