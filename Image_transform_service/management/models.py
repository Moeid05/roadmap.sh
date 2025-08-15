from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

class Image(models.Model) :
    title = models.CharField(unique=True , max_length=12)
    image = models.ImageField(upload_to='images/')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        if self.pk is not None:
            try:
                existing_image = Image.objects.get(pk=self.pk)
                if existing_image.image != self.image:
                    if existing_image.image:
                        existing_image.image.delete(save=False)  
            except ObjectDoesNotExist:
                pass 
        super().save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)
    def __str__(self):
        return self.title
