from django.db import models
from taggit.managers import TaggableManager
from colorfield.fields import ColorField

class ServiceModel(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100, default="")
    prefix = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images",
                              default="/static/referralroulette/missing.png")
    color = ColorField(default='#F5F5F5')
    text_color = ColorField(default='#212529')
    tags = TaggableManager()
    clicks = models.IntegerField()
    active = models.BooleanField()

class ReferralModel(models.Model):
    link = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    clicks = models.IntegerField()