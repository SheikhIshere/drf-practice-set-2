"""
Docstring for accounts.account_manager
"""
from django.contrib.auth.models import UserManager


class AccountManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email')
        email = self.normalize_email(email)
        user = self.model(email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)

        return user