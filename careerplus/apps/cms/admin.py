from django.contrib import admin

from .models import PageCategory, Tag, IndexerWidget, ColumnHeading,\
	IndexColumn, Widget, Page, PageWidget, Document, Comment, PageCounter


class PageCategoryAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'slug', 'is_active')
	list_filter = ()
	search_fields = ('name', 'slug', 'id')
	filter_horizontal = ()
	raw_id_fields = ('parent', 'created_by', 'last_modified_by')


class TagAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'slug', 'is_active')
	list_filter = ()
	search_fields = ('name', 'slug', 'id')
	filter_horizontal = ()
	raw_id_fields = ('parent', 'created_by', 'last_modified_by')


class ColumnHeadingAdmin(admin.StackedInline):
	model = ColumnHeading
	raw_id_fields = ('indexer',)


class IndexColumnAdmin(admin.StackedInline):
	model = IndexColumn
	raw_id_fields = ('indexer',)


class IndexerWidgetAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'heading')
	list_filter = ()
	search_fields = ('name', 'heading', 'id')
	filter_horizontal = ()
	inlines = [IndexColumnAdmin, ColumnHeadingAdmin]
	raw_id_fields = ('created_by', 'last_modified_by')


class WidgetAdmin(admin.ModelAdmin):
	list_display = ('id', 'widget_type', 'name', 'template_name', 'is_active',
		'is_external', 'is_pop_up', 'heading', 'redirect_url')
	list_filter = ('widget_type', )
	search_fields = ('name', 'heading', 'id')
	filter_horizontal = ()
	raw_id_fields = ('created_by', 'last_modified_by', 'user')


class DocumentAdminInline(admin.StackedInline):
	model = Document
	raw_id_fields = ('page', )


class PageAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'category', 'status', 'parent', 'slug',
		'total_view', 'total_download', 'total_share', 'active', 'allow_comment',
		'comment_count', 'publish_date')
	list_filter = ('category', 'status')
	search_fields = ('id', 'title', 'slug')
	filter_horizontal = ('tag', 'related_pages', 'widgets')
	raw_id_fields = ('parent', 'category', 'created_by', 'last_modified_by')
	inlines = [DocumentAdminInline]


class PageWidgetAdmin(admin.ModelAdmin):
	list_display = ('id', 'page', 'widget', 'section', 'ranking')
	list_filter = ('section', )
	search_fields = ('id',)
	filter_horizontal = ()
	raw_id_fields = ('created_by', 'last_modified_by', 'page', 'widget')


class CommentAdmin(admin.ModelAdmin):
	list_display = ('id', 'page', 'created_by', 'submit_date', 'is_published',
		'is_removed', 'replied_to')
	list_filter = ()
	search_fields = ('id', 'message')
	filter_horizontal = ()
	raw_id_fields = ('created_by', 'last_modified_by', 'page', 'replied_to')


class PageCounterAdmin(admin.ModelAdmin):
	list_display = ('id', 'page', 'count_period', 'no_views', 'no_downloads',
		'no_shares', 'added_on', 'modified_on')
	list_filter = ('count_period', )
	search_fields = ('id', 'count_period', 'no_shares', 'no_views')
	filter_horizontal = ()
	raw_id_fields = ('page', )


admin.site.register(PageCategory, PageCategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(IndexerWidget, IndexerWidgetAdmin)
admin.site.register(Widget, WidgetAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(PageWidget, PageWidgetAdmin)
admin.site.register(Comment, CommentAdmin)