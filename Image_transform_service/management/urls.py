from django.urls import path 
from .views import UploadImageView,RetrieveImageView,ImageListView,TransformImageView,TransformAndUpdateImageView
urlpatterns = [
    path('upload/',UploadImageView.as_view() ),
    path('<int:pk>/',RetrieveImageView.as_view() ),
    path('',ImageListView.as_view() ),
    path('<int:id>/transform/',TransformImageView.as_view() ),
    path('<int:id>/transform_and_update/',TransformAndUpdateImageView.as_view() ),
]
