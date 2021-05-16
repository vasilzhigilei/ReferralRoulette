from django.db import models
from taggit.managers import TaggableManager
from colorfield.fields import ColorField
from django.utils import timezone
from tinymce import models as tinymce_models

class ServiceModel(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=300, default="")
    referral_description = tinymce_models.HTMLField('Referral Description')
    company_description = tinymce_models.HTMLField('Company Description')
    prefix = models.CharField(max_length=200, default="", blank=True)
    default_link = models.CharField(max_length=200, default="")
    image = models.ImageField(upload_to="service_images",
                              default="/service_images/missing.png")
    background_color = ColorField(default='#F5F5F5')
    text_color = ColorField(default='#212529')
    tags = TaggableManager()
    clicks = models.IntegerField(default=0)
    code = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class ReferralModel(models.Model):
    service = models.CharField(max_length=30)
    slug = models.SlugField()
    link = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=50)
    clicks = models.IntegerField(default=0)

class CategoryModel(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)
    color = ColorField(default='#212529')
    image = models.ImageField(upload_to="category_images",
                              default="/category_images/missing.png")

class ContactModel(models.Model):
    from_email = models.EmailField()
    time = models.DateTimeField(blank=True, default=timezone.now)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=3000)