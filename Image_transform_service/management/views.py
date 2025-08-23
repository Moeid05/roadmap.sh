from rest_framework.generics import CreateAPIView ,ListAPIView ,GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializer import ImageSerializer
from .models import Image
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