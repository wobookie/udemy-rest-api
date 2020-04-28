from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
                                        BaseUserManager, \
                                        PermissionsMixin


class CustomUserManager(BaseUserManager):

    def create_user(self, username, email=None, password=None, **extra_fields):
        """Creates and saves a new users"""
        if not username:
            raise ValueError('Users must have user name')

        user = self.model(username=username,
                          email=self.normalize_email(email),
                          **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """Creates and saves a new users"""
        user = self.create_user(username, email, password)

        user.is_staff = True
        user.is_superuser = True

        user.save(using=self.db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
