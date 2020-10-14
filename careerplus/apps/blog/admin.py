from django.contrib import admin
from .models import Category, Tag, Blog, Comment


class BlogAdmin(admin.ModelAdmin):
	list_display = ('id', 'p_cat', 'name', 'status', 'score', 'publish_date', 'no_views', 'no_shares')
	list_filter = ('status', 'p_cat', 'visibility')
	search_fields = ('id', 'name')
	filter_horizontal = ('tags', 'sec_cat', 'speakers')
	raw_id_fields = ('created_by', 'last_modified_by', 'p_cat', 'user')
	prepopulated_fields = {"slug": ("name",)}


class CategoryAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'is_active', 'priority')
	list_filter = ('is_active', )
	search_fields = ('id', 'name')
	filter_horizontal = ()
	raw_id_fields = ('created_by', 'last_modified_by')


class TagAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'is_active', 'priority')
	list_filter = ('is_active', )
	search_fields = ('id', 'name')
	filter_horizontal = ()
	raw_id_fields = ('created_by', 'last_modified_by')
	prepopulated_fields = {"slug": ("name",)}


admin.site.register(Category)
admin.site.register(Tag, TagAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment)
