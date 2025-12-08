"""
Docstring for users.models
"""

# core imports
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager

# time related
from django.utils import timezone

"""manager for user"""
class AccountManager(UserManager):
    def create_user(self, email = ..., password = None, **extra_fields):
        if not email:
            raise ValueError("user must have email account")
        
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.set_default('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
    
"""main User model"""    
class Account(AbstractBaseUser):
    email = models.EmailField()
    name = models.CharField(max_length=True)

    date_joined = models.DateTimeField(default=timezone.now())

    is_active = True
    is_staff = False

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AccountManager()

    def __str__(self):
        return f'{self.email}'
