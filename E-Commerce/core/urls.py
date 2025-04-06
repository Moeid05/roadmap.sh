from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def custom_403_view(request, exception):
    return JsonResponse({'error': 'Forbidden', 'status': 403}, status=403)

def custom_404_view(request, exception):
    return JsonResponse({'error': 'Not Found', 'status': 404}, status=404)

def custom_500_view(request):
    return JsonResponse({'error': 'Server Error', 'status': 500}, status=500)
    
handler403 = custom_403_view
handler404 = custom_404_view
handler500 = custom_500_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('users.urls')),
    path('api/products/', include('products.urls')),
]