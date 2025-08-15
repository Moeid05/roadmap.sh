from django.contrib.auth.models import AbstractUser,PermissionsMixin
from django.db import models
from .managers import CustomUserManager
from management.models import Images
class CustomUser(AbstractUser,PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    images = models.ForeignKey(Images,on_delete=models.CASCADE)

    def __str__(self):
        return self.username