from django.contrib import admin

# Register your models here.
from .models import ServiceModel as S
from .models import ReferralModel as R

# import into admin
admin.site.register(S)
admin.site.register(R)
