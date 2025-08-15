from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_delete
from django.dispatch import receiver

class Image(models.Model):
    title = models.CharField(unique=True, max_length=12)
    image = models.ImageField(upload_to='images/')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def clean(self):
        # Custom validation logic
        if not self.title.isalnum():
            raise ValidationError("Title must be alphanumeric.")
    def save(self, *args, **kwargs):
        # Custom save logic can be added here if needed
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title
@receiver(pre_delete, sender=Image)
def delete_image_on_delete(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)