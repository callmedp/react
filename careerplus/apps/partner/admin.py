from django.contrib import admin
from . import models


class VendorHierarchyInline(admin.TabularInline):
	model = models.VendorHierarchy
	extra = 1


class VendorAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'slug', 'email', 'mobile', 'pan', 'website')

	inlines = [VendorHierarchyInline]

admin.site.register(models.Vendor, VendorAdmin)