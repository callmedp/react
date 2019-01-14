from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from . import models


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewed_item', 'user_email', 'created']
    list_filter = ['status', 'average_rating']
    search_fields = ['reviews__name']



class DetailPageWidgetAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']


class ReviewExtraInfoAdmin(admin.ModelAdmin):
    list_display = ['type', 'review', 'content_object']


admin.site.register(models.Review, ReviewAdmin)
admin.site.register(models.DetailPageWidget, DetailPageWidgetAdmin)
