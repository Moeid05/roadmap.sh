from django.contrib import admin
from django.urls import path
from .views import weather_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/<str:address>/', weather_api),
]