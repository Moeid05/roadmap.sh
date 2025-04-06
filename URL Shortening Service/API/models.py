from django.db import models
from django.utils import timezone
import string
import random

class Url(models.Model) :
    url = models.CharField(max_length=255)
    shorten = models.CharField(max_length=10,unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    access_count = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if not self.shorten:
            self.shorten = self.generate_short_code()
        super().save(*args, **kwargs)
    def update(self,url) :
        self.url = url
        self.updated_date = timezone.now()
        self.save()

    def increment_access_count(self):
        self.access_count += 1
        self.save()

    def generate_short_code(self):
        length = 6
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    @property
    def as_json(self):  
        return {
            'id': self.id,
            'url': self.url,
            'shorten': self.shorten,
            'created_date': self.created_date,
            'updated_date': self.updated_date,
        }
    @property
    def stats(self):
        return {
            'id': self.id,
            'url': self.url,
            'shorten': self.shorten,
            'created_date': self.created_date,
            'updated_date': self.updated_date,
            'access_count': self.access_count,
                }