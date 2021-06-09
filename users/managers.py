from django.contrib.auth.models import BaseUserManager
import re


class CustomUserManager(BaseUserManager):
    EMAIL_REGEXP = re.compile(r"[^@]+@[^@]+\.[^@]+")

    def validate_email(self, email):
        email = self.normalize_email(email)
        match = re.match(self.EMAIL_REGEXP, email)
        if match is None:
            raise ValueError('Email must match email pattern')
        else:
            return email

    def validate_password(self, password):
        if len(password) < 8:
            raise ValueError('Password must be more than 7 char')
        else:
            return password

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if email is None:
            raise ValueError('The Email must be set')
        email = self.validate_email(email)
        password = self.validate_password(password)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)
