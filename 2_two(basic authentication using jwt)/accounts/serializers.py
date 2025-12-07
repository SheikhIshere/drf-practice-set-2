
"""
Docstring for accounts.serializers
"""

# core import
from rest_framework import serializers
from django.contrib.auth import get_user_model

# authentication import
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# user
User = get_user_model()



"""
all user
"""
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'is_active', 'is_staff', 'date_joined')


"""
registration
"""
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    password2 = serializers.CharField(write_only = True)
    
    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'password2',
        )
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "error": "password didn't matched"
            })
        validate_password(attrs['password'])

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2', None)
        password = validated_data.pop('password')

        return User.objects.create_user(password=password, **validated_data)



"""
log in 
"""
class LoginTokenObtainSerializer(TokenObtainPairSerializer):
    """
    Docstring for LoginSerializer
    """ 
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data

        return data
    















