from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_delete
from django.dispatch import receiver

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='images',
                                blank=True,
                                null=True)
    @property
    def image_url_with_placeholder(self):
        return f"http://127.0.0.1:8000/images/{self.id}"
    def clean(self):
        if self.user is None:
            raise ValidationError("User must be specified.")
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
@receiver(pre_delete, sender=Image)
def delete_image_on_delete(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)