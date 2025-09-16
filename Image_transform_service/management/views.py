import io
import base64
from django.core.files.base import ContentFile
from django.conf import settings
from django.http import FileResponse
from django.core.cache import cache
from rest_framework.generics import CreateAPIView ,ListAPIView ,GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django_ratelimit.decorators import ratelimit
import hashlib
import json
from .serializer import ImageSerializer ,TransformImageSerializer
from .models import Image
from .tasks import transform_image_task
from .transformer import transform_instance_image
from django.utils.decorators import method_decorator
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

@method_decorator(ratelimit(key='user', rate='10/m'),name='dispatch')
class TransformImageView(APIView):
    permission_classes = [IsAuthenticated] #auth just for ratelimit
    def post(self ,request ,id):
        data = request.data
        data['image_id'] = id
        serializer = TransformImageSerializer(data=request.data)
        if serializer.is_valid():
            transforms = serializer.get_transforms()
            
            transforms_json = json.dumps(transforms, sort_keys=True)
            cache_key = f"transformed_image_{id}_{hashlib.md5(transforms_json.encode()).hexdigest()}"
            
            cached_img_content = cache.get(cache_key)
            if cached_img_content:
                return FileResponse(cached_img_content, content_type='image/jpeg')
            # try:
            if settings.USE_CELERY:
                result = transform_image_task.delay(id, transforms)
                task_result = result.get()
                if task_result.get('status') == 'error':
                    return Response({"error": task_result.get('message')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                img_base64 = task_result.get('transformed_image')
                img_format = task_result.get('img_format') or 'PNG'
                img_bytes = base64.b64decode(img_base64)
                img_io = io.BytesIO(img_bytes)
                img_io.seek(0)
                img_content = ContentFile(img_io.read(), name=f'transformed.{img_format.lower()}')
                cache.set(cache_key, img_content, timeout=600)
                img_io.seek(0)
                return FileResponse(img_io, content_type=f'image/{img_format.lower()}')
            else:
                result = transform_image_task(id, transforms)
                image_instance = Image.objects.get(id=id).image
                transformed_image,img_format = transform_instance_image(image_instance, transforms)
                img_io = io.BytesIO()
                transformed_image.save(img_io, format = img_format or 'PNG')
                img_content = ContentFile(img_io.getvalue(), name=f'transformed.{img_format.lower() if img_format else "jpeg"}')
                cache.set(cache_key, img_content, timeout=600)
                return FileResponse(img_content , content_type='image/jpeg')
            # except Exception as e:
            #     return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(ratelimit(key='user', rate='10/m'),name='dispatch')
class TransformAndUpdateImageView(APIView) : 
    #just for ratelimit
    permission_classes = [IsAuthenticated]
    def post(self ,request ,id):
        data = request.data
        data['image_id'] = id
        serializer = TransformImageSerializer(data=request.data)
        if serializer.is_valid():
            transforms = serializer.get_transforms()
            image_instance = serializer.get_image_instance().image
            try:
                new_image,img_format = transform_image_task.delay(image_instance, transforms)
                serializer.update_image(new_image,img_format)
                return FileResponse(serializer.get_image_instance().image.open(),content_type='image/jpeg')
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
