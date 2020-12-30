from django.contrib import admin

# Register your models here.
from .models import ServiceModel
from .models import ReferralModel

@admin.register(ServiceModel)
class ServiceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ReferralModel)
class ReferralAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('service',)}

admin.site.unregister(ServiceModel)
admin.site.unregister(ReferralModel)
# import into admin
admin.site.register(ServiceModel, ServiceAdmin)
admin.site.register(ReferralModel)