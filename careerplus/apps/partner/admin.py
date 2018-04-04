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

    extra = 0


class CeritficateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'skill')
    model = models.Certificate


class UserCertificateAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'candidate_email', 'candidate_mobile')
    model = models.UserCertificate


admin.site.register(models.Vendor, VendorAdmin)
admin.site.register(models.Certificate, CeritficateAdmin)
admin.site.register(models.UserCertificate, UserCertificateAdmin)
