from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    UserManager
)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Create your models here.


"""custom user manager"""
class AccountManager(UserManager):
    def create_user(self, email, password , **extra_fields):
        """creating user here"""
        if not email:
            raise ValueError(_('The email must be set'))
        
        # email = self.normalize_email(email)
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Creates and saves a superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)





"""custom user"""
class User(AbstractBaseUser, PermissionsMixin):
    """here i am defining the custom user"""
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True, blank=True)
    name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects =  AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


    def generate_uniq_username(self):
        """here i am predefining the user name"""
        if self.username:
            return
        
        base = self.email.split('@')[0].lower()
        username = base

        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base}{counter}"
            counter += 1
        
        self.username = username
    
    # Auto-call this before every save
    def save(self, *args, **kwargs):
        self.generate_uniq_username()
        super().save(*args, **kwargs)        
