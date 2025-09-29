from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('scores/',include('scores.url'))
    path('users/',include('users.url'))
]
