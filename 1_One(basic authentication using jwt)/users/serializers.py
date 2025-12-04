"""
Docstring for users.serializers
"""

# core imports
from rest_framework import serializers
from django.contrib.auth import get_user_model

# authentication
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# local imports
from .models import User

User = get_user_model()




"""
user serializer to represent users in json
"""
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'username',
            'is_staff', 'is_active', 'date_joined'
        )
        read_only_fields = (
            'id', 'username', 'is_staff',
            'is_active', 'date_joined'
        )


"""
user registration serializer
"""
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    password2 = serializers.CharField(write_only = True)

    class Meta: 
        model = User
        fields = (
            'email',
            'name',
            'password',
            'password2',
        )
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {
                    'password': "password doesn't match"
                }
            )
        validate_password(attrs['password'])
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2', None)
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)

        return user
    

"""
token for authenticate
"""
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data


"""
changing user's password
"""
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only = True)
    new_password = serializers.CharField(write_only = True)

    def validate_new_password(self, value):
        validate_password(value)

        return value