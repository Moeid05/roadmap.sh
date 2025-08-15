from rest_framework import serializers
from .models import Image

class Image_uploader_serializer(serializers.ModelSerializer) :

    class meta :
        model = Image
        fields = ['id', 'title', 'image', 'user']
    def validate_image(self,value) :
        if value.size > 5 * 1024 * 1024 :
            raise serializers.ValidationError("File size must be under 5MB.")
        return value
