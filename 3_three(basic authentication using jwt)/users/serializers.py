"""
Docstring for users.serializers
"""

# core imports 
from rest_framework import serializers, status

# validation
from django.contrib.auth.password_validation import validate_password

# local imports
from .models import (
    Account
)

# jwt imports
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer





"""showing list of user"""
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'id', 'email', 
            'name', 
            'date_joined', 
            'is_active', 
            'is_staff',
        )


"""serializer for registration"""
# class UserRegistration(serializers.Serializer):
#     email = serializers.EmailField(write_only = True)
#     password = serializers.CharField(write_only = True)
#     password2 = serializers.CharField(write_only = True)
    
#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({
#                 'error': "password didn't matched"
#             })
#         validate_password(attrs['password'])

#         return attrs
    
#     def create(self, validated_data):
#         email = validated_data['email']
#         validated_data.pop('password2', None)
#         password = validated_data['password']

#         if Account.objects.filter(email=email).exists():
#             raise serializers.ValidationError('Email already exist')
        
#         return Account.objects.create_user(email=email, password=password, **validated_data)

"""this is a great approach but not better then code 2"""
"""
user registration serializer
"""
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    password2 = serializers.CharField(write_only = True)
    
    class Meta:
        model = Account
        fields = (
            'email',
            'password',
            'password2',
        )
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'error': "Password doesn't matched"
            })
        validate_password(attrs['password'])

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2', None)
        password = validated_data.pop('password')

        return Account.objects.create_user(
            password=password, **validated_data
        )
    



"""
user login serializer
"""
class LoginTokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserListSerializer(self.user).data

        return data
    

""" password change serializer """
class ChangePasswordSerializer(serializers.Serializer):
    """here i am taking input old password and new password"""
    old_password = serializers.CharField(write_only = True, required=True)
    new_password = serializers.CharField(write_only = True, required=True)
    confirm_new_password = serializers.CharField(write_only = True, required=True)

    def validate(self, attrs):
        """here i am validating is password is similler or not"""
        if attrs['new_password'] == attrs[['old_password']]:
            raise serializers.ValidationError({
                'error': 'old password and new password must not be same.'
            })

        if attrs['new_password'] != attrs[['confirm_new_password']]:
            raise serializers.ValidationError({
                'error': 'New password and confirm password must match.'
            })
        validate_password(attrs['new_password'])
        return attrs