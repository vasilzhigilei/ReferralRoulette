from django.db import models
from taggit.managers import TaggableManager
from colorfield.fields import ColorField

class ServiceModel(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=100, default="")
    prefix = models.CharField(max_length=100)
    image = models.ImageField(upload_to="service_images",
                              default="/service_images/missing.png")
    background_color = ColorField(default='#F5F5F5')
    text_color = ColorField(default='#212529')
    tags = TaggableManager()
    clicks = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ReferralModel(models.Model):
    service = models.CharField(max_length=30)
    link = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    clicks = models.IntegerField(default=0)