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
    raw_id_fields = ('city', 'country','state')
    extra = 0


class CeritficateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'skill', "vendor_provider")
    model = models.Certificate


class UserCertificateAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'year', 'candidate_email',
        'candidate_mobile', 'certificate', "get_vendor")
    model = models.UserCertificate

    def get_vendor(self, obj):
        return obj.certificate.vendor_provider
    get_vendor.short_description = 'Vendor'


admin.site.register(models.Vendor, VendorAdmin)
admin.site.register(models.Certificate, CeritficateAdmin)
admin.site.register(models.UserCertificate, UserCertificateAdmin)
