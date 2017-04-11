from django.contrib import admin

from .models import SkillPage


class PageAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'parent', 'slug',
		'total_view', 'total_download', 'total_share', 'is_active', 'allow_comment',
		'comment_count', 'publish_date')
	search_fields = ('id', 'name', 'slug')
	filter_horizontal = ('widgets', )
	raw_id_fields = ('parent', 'created_by', 'last_modified_by')


admin.site.register(Page, PageAdmin)
