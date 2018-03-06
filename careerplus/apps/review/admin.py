from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from . import models


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewed_item', 'user_email', 'created']


class DetailPageWidgetAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']


class ReviewExtraInfoAdmin(admin.ModelAdmin):
    list_display = ['type', 'review', 'content_object']


admin.site.register(models.Review, ReviewAdmin)
admin.site.register(models.DetailPageWidget, DetailPageWidgetAdmin)
