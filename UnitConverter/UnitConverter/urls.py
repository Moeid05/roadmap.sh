from django.contrib import admin
from django.urls import path
from .views import Converter
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Converter.as_view(),name='converter')
]
