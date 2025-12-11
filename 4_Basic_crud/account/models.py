"""
Docstring for account.models
"""

# core imports
from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4

"""base user account"""
class Account(AbstractUser):
    """here i am making the user attributes"""
    # personal info
    email = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    # image = models.ImageField(null=True) # lt's skip it for now

    # system configure
    USERNAME_FIELD = "email" 
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if not self.username:
            while True:
                self.username = f"user_{uuid4().hex[:12]}"
                if not Account.objects.filter(username=self.username).exists():
                    break
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.email