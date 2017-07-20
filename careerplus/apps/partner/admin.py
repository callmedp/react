from django.contrib import admin
from . import models


class VendorHierarchyInline(admin.TabularInline):
	model = models.VendorHierarchy
	extra = 1


class VendorAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'slug', 'email', 'mobile', 'pan', 'website')

	inlines = [VendorHierarchyInline]
    model = models.VendorHierarchy
    fk_name = 'vendee'
    readonly_fields = ('modified',)
    raw_id_fields = ['vendee', 'employee']
    
    extra = 0



admin.site.register(models.Vendor, VendorAdmin)