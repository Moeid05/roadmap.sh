from rest_framework import generics ,status
from rest_framework.permissions import IsAuthenticated,IsAdminUser 
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product
from .serializers import *
#from .serializers import CreateProductSerializer, AddCartItemSerializer, EditCartItemSerializer, RemoveCartItemSerializer, ProductSerializer, CartItemSerializer,CheckoutSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class CreateProductView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        serializer = CreateProductSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            product = serializer.save()
            return Response({"id": product.id, "name": product.name, "price": product.price}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddCartItemView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = AddCartItemSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            cart_item = serializer.create(serializer.validated_data)
            return Response({"message": "Item added to cart", "cart_item_id": cart_item.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartItemView(APIView):
    permission_classes = [IsAuthenticated]
    #update
    def put(self, request, item_id):
        data = request.data.copy()
        data['item_id'] = item_id 
        serializer = EditCartItemSerializer(data=data,context={'request': request})
        if serializer.is_valid():
            cart_item = serializer.update_cart(item_id, serializer.validated_data)
            return Response({"message": "cart edited", "cart_item_id": cart_item.id, "cart_item_name": cart_item.product.name, "cart_item_quantity": cart_item.quantity}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #delete
    def delete(self, request, item_id):
        serializer = RemoveCartItemSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            response_data = serializer.Delete(item_id,serializer.validated_data)
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShowAllProducts(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class CartItemsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = CartItemsAuthSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            cart_items = serializer.get_cart_items()
            cart_item_serializer = CartItemSerializer(cart_items, many=True)
            return Response({'cart_items': cart_item_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = CheckoutSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            checkout_session = serializer.checkout(serializer.validated_data)
        return Response({'id': checkout_session.id}, status=status.HTTP_200_OK)