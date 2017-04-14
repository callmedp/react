from django.contrib import admin
from .models import Category, Tag, Blog


class BlogAdmin(admin.ModelAdmin):
	list_display = ('id', 'p_cat', 'name', 'status', 'score', 'publish_date', 'no_views', 'no_shares')
	list_filter = ('status', 'p_cat')
	search_fields = ('id', 'name')
	filter_horizontal = ('tags', 'sec_cat')
	raw_id_fields = ('created_by', 'last_modified_by', 'p_cat', 'user')


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Blog, BlogAdmin)