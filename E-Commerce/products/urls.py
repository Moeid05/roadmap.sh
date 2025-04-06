from django.urls import path
from .views import CreateProductView, AddCartItemView, ShowAllProducts,CartItemsAPIView,CartItemView,CreateCheckoutSessionView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
   path('create_product/', csrf_exempt(CreateProductView.as_view()),),
   path('add_to_cart/', AddCartItemView.as_view()),
   path('<int:item_id>/', CartItemView.as_view()),
   path('view_products/', ShowAllProducts.as_view()),
   path('my_cart/', CartItemsAPIView.as_view()),
   path('checkout/', CreateCheckoutSessionView.as_view()),

]
