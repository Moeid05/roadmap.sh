import io
import base64
from celery import shared_task
from .transformer import transform_instance_image
from .models import Image
from django.conf import settings
@shared_task
def transform_image_task(image_id, transforms):
    try:
        image_instance = Image.objects.get(id=image_id).image
        transformed_image, img_format = transform_instance_image(image_instance, transforms)
        img_io = io.BytesIO()
        transformed_image.save(img_io, format=img_format)
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.read()).decode('utf-8')
        return {
            'status': 'success',
            'transformed_image': img_base64,
            'img_format': img_format
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }
