from django.contrib.auth.models import AbstractUser,PermissionsMixin
from django.db import models
from .managers import CustomUserManager

class CustomUser(AbstractUser,PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def remove_item_from_cart(self, product_id):
        try:
            cart_item = self.cart_items.get(product_name_id=product_id)
            cart_item.delete()
            return True
        except CartItem.DoesNotExist:
            return False