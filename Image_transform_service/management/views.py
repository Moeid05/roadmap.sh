from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializer import Image_uploader_serializer
from .models import Image
class UploadImage(CreateAPIView) :
    queryset = Image.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = Image_uploader_serializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)