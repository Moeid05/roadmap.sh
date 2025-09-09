import io
from django.core.files.base import ContentFile
from rest_framework import serializers
from .models import Image

class ImageSerializer(serializers.ModelSerializer) :

    class Meta :
        model = Image
        fields = ['id' ,'image' ,'user']
    def validate_image(self,value) :
        if value.size > 5 * 1024 * 1024 :
            raise serializers.ValidationError("File size must be under 5MB.")
        return value
    
    def get_username(self, obj):
        return obj.user.username if obj.user else None
        

#transformer

from rest_framework import serializers

class ResizeSerializer(serializers.Serializer):
    width = serializers.IntegerField(min_value=1)
    height = serializers.IntegerField(min_value=1)

class CropSerializer(serializers.Serializer):
    width = serializers.IntegerField(min_value=1)
    height = serializers.IntegerField(min_value=1)
    x = serializers.IntegerField()
    y = serializers.IntegerField()

class WatermarkSerializer(serializers.Serializer):
    text = serializers.CharField()
    position = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=2,
        max_length=2
    )

class FiltersSerializer(serializers.Serializer):
    grayscale = serializers.BooleanField(default=False)
    sepia = serializers.BooleanField(default=False)
    blur = serializers.BooleanField(default=False)
    sharpen = serializers.BooleanField(default=False)

class CompressSerializer(serializers.Serializer):
    quality = serializers.IntegerField(min_value=1, max_value=100)

class TransformationsSerializer(serializers.Serializer):
    resize = ResizeSerializer(required=False)
    crop = CropSerializer(required=False)
    rotate = serializers.IntegerField(required=False)
    watermark = WatermarkSerializer(required=False)
    flip = serializers.BooleanField(required=False)
    mirror = serializers.BooleanField(required=False)
    format = serializers.ChoiceField(choices=['jpeg', 'png'])
    filters = FiltersSerializer(required=False)
    compress = CompressSerializer(required=False)

class TransformImageSerializer(serializers.Serializer):
    image_id = serializers.IntegerField()
    transformations = TransformationsSerializer()

    def get_transforms(self):
        return self.validated_data.get('transformations', {})

    def get_image_instance(self) :
        image_id = self.validated_data.get('image_id')
        try:
            return Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            raise serializers.ValidationError(f"Image with id {image_id} does not exist.")
        
    def update_image(self, new_image, img_format=None):
        image_id = self.validated_data.get('image_id')
        try:
            instance = Image.objects.get(id=image_id)
            img_io = io.BytesIO()
            new_image.save(img_io, format = img_format or 'PNG')
            img_content = ContentFile(img_io.getvalue(), name=f'image_{image_id}.{img_format.lower() if img_format else "jpeg"}')
            instance.image.save(img_content.name, img_content, save=True)
        except Image.DoesNotExist:
            raise serializers.ValidationError(f"Image with id {image_id} does not exist.")
        except Exception as e:
            raise serializers.ValidationError(str(e))