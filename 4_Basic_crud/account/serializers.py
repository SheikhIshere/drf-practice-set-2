"""
Docstring for account.serializers
"""

# core imports
from rest_framework import (
    serializers
)
from rest_framework.exceptions import ValidationError

# local imports
from .models import Account # this and User is same
from django.contrib.auth import get_user_model
User = get_user_model()

# password validation
from django.contrib.auth import password_validation

# jwt authentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



"""retrieve all user"""
class AllUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'name',
            'is_active',
            'date_joined'
        )
    
    def get_name(self, obj):
        return f'{obj.first_name + obj.last_name}'.strip()


"""register serializer"""
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'password2'
        )
    
    def validate(self, attrs):
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({
                'error':'email already exist'
            })

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'error': 'both password must match'
            })
        password_validation(attrs['password'])
        return attrs
    
    def create(self, validated_data):
        # let's make you agh!
        validated_data.pop('password', None)
        password = validated_data.pop('password2')

        return User.objects.create_user(password=password, **validated_data)
    

"""user login"""    
class LoginSerializer(TokenObtainPairSerializer):
    """logging in user """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = AllUserSerializer(self.user).data
        return data


"""password change"""    
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only = True)
    new_password = serializers.CharField(write_only = True)
    new_password2 = serializers.CharField(write_only = True)

    def validate(self, attrs):
        # getting user
        user = self.context['request'].user

        # checking is old password valid or not
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({
                'error': 'old password is incorrect'
            })

        if attrs['old_password'] == attrs['new_password']:
            raise serializers.ValidationError({
                'error':'old and new password must not be same'
            })
        
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({
                'error': 'both new password must match'
            })
        password_validation(attrs['new_password'])
        
        return attrs