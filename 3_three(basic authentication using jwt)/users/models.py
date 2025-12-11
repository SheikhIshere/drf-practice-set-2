"""
Docstring for users.models
"""

# core imports
from typing import Required
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

"""manager for user"""
class AccountManager(BaseUserManager):
    def create_user(self, email = ..., password = None, **extra_fields):
        if not email:
            raise ValueError("user must have email account")
        
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
            
        # Get or set the name
        name = extra_fields.pop('name', 'Admin')
            
        return self.create_user(email, name=name, password=password, **extra_fields)
    
"""main User model"""    
class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)

    date_joined = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 

    objects = AccountManager()

    def __str__(self):
        return f'{self.email}'
