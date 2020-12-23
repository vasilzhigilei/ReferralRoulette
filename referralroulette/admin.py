from django.contrib import admin

# Register your models here.
from .models import ServiceModel
from .models import ReferralModel

@admin.register(ServiceModel)
class ServiceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.unregister(ServiceModel)
# import into admin
admin.site.register(ServiceModel, ServiceAdmin)
admin.site.register(ReferralModel)