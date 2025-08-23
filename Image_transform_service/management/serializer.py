from rest_framework import serializers
from .models import Image

class ImageSerializer(serializers.ModelSerializer) :

    class Meta :
        model = Image
        fields = ['id', 'image', 'user']
    def validate_image(self,value) :
        if value.size > 5 * 1024 * 1024 :
            raise serializers.ValidationError("File size must be under 5MB.")
        return value
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
    
    def get_username(self, obj):
        return obj.user.username if obj.user else None