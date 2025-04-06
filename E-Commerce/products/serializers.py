from rest_framework import serializers
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .models import Product, CartItem
from django.conf import settings
import stripe

class CreateProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        model = Product
        fields = ['name','price']
        
    def create(self, validated_data):
        product = Product(**validated_data)
        product.save()
        return product

class AddCartItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_quantity = serializers.IntegerField()

    def validate(self, attrs):
        user = self.context['request'].user
        if user is None:
            raise serializers.ValidationError("Invalid username or password.")
        elif user.is_authenticated:
            attrs['user'] = user
        product_id = attrs.get('product_id')
        get_object_or_404(Product, id=product_id)
        product_quantity = attrs.get('product_quantity')

        if product_quantity <= 0:
            raise serializers.ValidationError("Product quantity must be a positive integer.")
        return attrs

    def create(self, validated_data):
        user = validated_data['user']
        product_id = validated_data['product_id']
        product_quantity = validated_data['product_quantity']
        cart_item, created = CartItem.objects.get_or_create(
            user=user,
            product=Product.objects.get(id=product_id),
            defaults={'quantity': product_quantity}
        )
        if not created:
            cart_item.quantity += product_quantity
            cart_item.save()
        return cart_item

class EditCartItemSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    item_new_quantity = serializers.CharField()

    def validate(self, attrs):
        user = self.context['request'].user
        if user is None:
            raise serializers.ValidationError("Invalid username or password.")
        elif user.is_authenticated:
            attrs['user'] = user
        item_id = attrs.get('item_id')
        item_new_quantity = attrs.get('item_new_quantity')
        
        user = authenticate(username=username, password=password)

        if int(item_new_quantity )<= 0:
            raise serializers.ValidationError("Product quantity must be a positive integer.")

        get_object_or_404(CartItem, id=item_id,user=user)
        return attrs

    def update_cart(self,item_id, validated_data):
        user = validated_data.get('user')
        item_new_quantity = validated_data.get('item_new_quantity')
        cart_item = CartItem.objects.get(id=item_id, user=user)
        cart_item.set_quantity(item_new_quantity)
        cart_item.save()
        return cart_item

class RemoveCartItemSerializer(serializers.Serializer):

    def validate(self, attrs):
        user = self.context['request'].user
        if user is None:
            raise serializers.ValidationError("Invalid username or password.")
        elif user.is_authenticated:
            attrs['user'] = user
        return attrs
    def Delete(self, item_id, validated_data):
        user = validated_data['user']
        cart_item = get_object_or_404(CartItem, user=user, id=item_id)
        cart_item.delete()
        return CartItem.objects.filter(user=user)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

class CartItemsAuthSerializer(serializers.Serializer):
    def validate(self, attrs):
        user = self.context['request'].user
        if user is None:
            raise serializers.ValidationError("Invalid username or password.")
        elif user.is_authenticated:
            attrs['user'] = user

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        attrs['user'] = user
        return attrs

    def get_cart_items(self):
        user = self.validated_data['user']
        return CartItem.objects.filter(user=user)
stripe.api_key = settings.STRIPE_SECRET_KEY

class CheckoutSerializer(serializers.Serializer):

    def validate(self, attrs):
        user = self.context['request'].user
        if user is None or not user.is_authenticated:
            raise serializers.ValidationError("Invalid username or password.")  
        cart_items = CartItem.objects.filter(user=user)
        if not cart_items.exists():
            raise serializers.ValidationError("Your cart is empty.")
        
        line_items = []
        for item in cart_items:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product.name,
                    },
                    'unit_amount': int(item.product.price *item.quantity* 100),
                },
                'quantity': item.quantity,
            })
        attrs['line_items'] = line_items
        return attrs
    def checkout(self,validated_data):
        YOUR_DOMAIN = "http://localhost:8000/api/checkout"
        return stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=validated_data.get("line_items"),
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )