from django.core.files.base import ContentFile
import io
import os
from django.conf import settings 
from django.http import FileResponse
from rest_framework.generics import CreateAPIView ,ListAPIView ,GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializer import ImageSerializer ,TransformImageSerializer
from .models import Image
from . import transformer

class UploadImageView(CreateAPIView) :
    queryset = Image.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ImageSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RetrieveImageView(GenericAPIView):
    queryset = Image.objects.all()
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        response = FileResponse(instance.image.open(), content_type='image/jpeg')
        response['Content-Disposition'] = f'attachment; filename="{instance.image.name}"'
        return response
        
class ImagePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    def get_paginated_response(self, data):
        for item in data:
            image_id = item['id']
            #f'{url}/images/{image_id}'
            item['image'] = f'http://127.0.0.1:8000/images/{image_id}'
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data,
        })
class ImageListView(ListAPIView):
    queryset = Image.objects.all().order_by('-id')
    serializer_class = ImageSerializer
    pagination_class = ImagePagination


class TransformImageView(APIView):
    def post(self ,request ,id):
        data = request.data
        data['image_id'] = id
        serializer = TransformImageSerializer(data=request.data)
        if serializer.is_valid():
            transforms = serializer.get_transforms()
            image_instance = serializer.get_image_instance().image
            storage = settings.STORAGE
            # try:
            transformed_image,img_format = transformer.transform_instance_image(image_instance, transforms)
            img_io = io.BytesIO()
            transformed_image.save(img_io, format = img_format or 'PNG')
            img_content = ContentFile(img_io.getvalue(), name=f'transformed.{img_format.lower() if img_format else "jpeg"}')
            return FileResponse(img_content , content_type='image/jpeg')
        #     except Exception as e:
        #         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class TransformAndUpdateImageView(APIView) : 
    def post(self ,request ,id):
        data = request.data
        data['image_id'] = id
        serializer = TransformImageSerializer(data=request.data)
        if serializer.is_valid():
            transforms = serializer.get_transforms()
            image_instance = serializer.get_image_instance().image
            try:
                new_image,img_format = transformer.transform_instance_image(image_instance, transforms)
                serializer.update_image(new_image,img_format)
                return FileResponse(serializer.get_image_instance().image.open(),content_type='image/jpeg')
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
