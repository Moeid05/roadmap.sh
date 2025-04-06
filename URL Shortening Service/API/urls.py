from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.shorten, name='shorten_url'),
    path('<str:shorten>/', views.shorten, name='shorten_detail'),
    path('<str:shorten>/stats/', views.stats, name='url_stats'),
]