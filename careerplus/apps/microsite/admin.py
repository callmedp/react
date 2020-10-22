from django.contrib import admin

from .models import MicroSite, MicrositeBanner, PartnerPage,\
    PartnerTestimonial, PartnerFaq


class PartnerPageAdmin(admin.ModelAdmin):
    filter_horizontal = ('banner_image',)

class MicrositeAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)

class PartnerTestimonialAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', )
    autocomplete_lookup_fields = { 'fk': ['user'], }

admin.site.register(MicroSite, MicrositeAdmin)
admin.site.register(MicrositeBanner)
admin.site.register(PartnerPage, PartnerPageAdmin)
admin.site.register(PartnerTestimonial, PartnerTestimonialAdmin)
admin.site.register(PartnerFaq)
