from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager
# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField(
        max_length=64, default=None, blank=True, null=True)
    last_name = models.CharField(
        max_length=64, default=None, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    date_birthday = models.DateTimeField(default=None, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
