from django.urls import path 
from .views import UploadImageView,RetrieveImageView,ImageListView
urlpatterns = [
    path('upload/',UploadImageView.as_view() ),
    path('<int:pk>/',RetrieveImageView.as_view() ),
    path('',ImageListView.as_view() ),
    # path('transform/<str : title>/transform/', ),
    # path('transform/<str : title>/', ),
]
