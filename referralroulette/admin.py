from django.contrib import admin

# Register your models here.
from .models import ServiceModel, ReferralModel, CategoryModel, ContactModel

@admin.register(ServiceModel)
class ServiceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ReferralModel)
class ReferralAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('service',)}

@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class ContactAdmin(admin.ModelAdmin):
    readonly_fields = ('time',)

# unregister
admin.site.unregister(ServiceModel)
admin.site.unregister(ReferralModel)
admin.site.unregister(CategoryModel)

# import into admin
admin.site.register(ServiceModel, ServiceAdmin)
admin.site.register(ReferralModel, ReferralAdmin)
admin.site.register(CategoryModel, CategoryAdmin)

admin.site.register(ContactModel, ContactAdmin)