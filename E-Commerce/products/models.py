from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User  = get_user_model()

class Product(models.Model) :
    name = models.CharField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class CartItem(models.Model) :
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"
  
    def set_quantity(self,quantity) :
        self.quantity = quantity if int(quantity) >1 else 1