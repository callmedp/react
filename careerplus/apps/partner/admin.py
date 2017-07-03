from django.contrib import admin
from . import models


class VendorHierarchyInline(admin.TabularInline):
    model = models.VendorHierarchy
    fk_name = 'vendee'
    readonly_fields = ('modified',)
    raw_id_fields = ['vendee', 'employee']
    
    extra = 0


class VendorAdmin(admin.ModelAdmin):
    inlines = (VendorHierarchyInline,)
    

admin.site.register(models.Vendor, VendorAdmin)