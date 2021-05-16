from django.contrib import admin

# Register your models here.
from .models import ServiceModel, ReferralModel, ContactModel

@admin.register(ServiceModel)
class ServiceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ReferralModel)
class ReferralAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('service',)}

class ContactAdmin(admin.ModelAdmin):
    readonly_fields = ('time',)

# unregister
admin.site.unregister(ServiceModel)
admin.site.unregister(ReferralModel)

# import into admin
admin.site.register(ServiceModel, ServiceAdmin)
admin.site.register(ReferralModel, ReferralAdmin)

admin.site.register(ContactModel, ContactAdmin)