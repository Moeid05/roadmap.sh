from django.contrib.auth.models import AbstractUser,PermissionsMixin
from django.db import models
from .managers import CustomUserManager
from management.models import Image
class CustomUser(AbstractUser,PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username