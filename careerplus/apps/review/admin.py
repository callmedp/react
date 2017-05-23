from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from . import models


class RatingAdmin(admin.ModelAdmin):
    list_display = ['review', 'category', 'value', ]
    raw_id_fields = ['review', ]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewed_item', 'user_email', 'created']


class ReviewExtraInfoAdmin(admin.ModelAdmin):
    list_display = ['type', 'review', 'content_object']


class ReviewCategoryChoiceAdmin(admin.ModelAdmin):
    list_display = ['ratingcategory', 'value', 'get_label']
    list_select_related = []

    def get_label(self, obj):
        return obj.label
    get_label.short_description = _('Label')


admin.site.register(models.Rating, RatingAdmin)
admin.site.register(models.RatingCategory)
admin.site.register(models.Review, ReviewAdmin)
admin.site.register(models.RatingCategoryChoice, ReviewCategoryChoiceAdmin)
