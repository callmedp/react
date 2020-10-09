from django.contrib import admin

from .models import IndexerWidget, ColumnHeading,\
    IndexColumn, Widget, Page, PageWidget, Document, Comment, PageCounter


class ColumnHeadingAdmin(admin.TabularInline):
    model = ColumnHeading
    raw_id_fields = ('indexer',)
    extra = 3
    max_num = 3


class IndexColumnAdmin(admin.StackedInline):
    model = IndexColumn
    raw_id_fields = ('indexer',)
    extra = 1


class IndexerWidgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'heading')
    list_filter = ()
    search_fields = ('heading', 'id')
    filter_horizontal = ()
    inlines = [ColumnHeadingAdmin, IndexColumnAdmin]
    raw_id_fields = ('created_by', 'last_modified_by')


class WidgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'widget_type', 'is_active',
        'display_name', 'heading', 'redirect_url', 'is_external', 'is_pop_up')
    list_filter = ('widget_type', )
    search_fields = ('heading', 'id')
    filter_horizontal = ['related_article', ]
    # raw_id_fields = ('created_by', 'last_modified_by', 'user', 'iw')


class DocumentAdminInline(admin.TabularInline):
    model = Document
    raw_id_fields = ('page', )
    extra = 1


class PageWidgetAdminInline(admin.TabularInline):
    model = PageWidget
    list_display = ('widget', 'section', 'ranking')
    raw_id_fields = ('widget', )
    extra = 1


class PageWidgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'page', 'widget', 'section', 'ranking')
    list_filter = ('section', )
    search_fields = ('id',)
    filter_horizontal = ()
    raw_id_fields = ('created_by', 'last_modified_by', 'page', 'widget')


class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'slug',
        'total_view', 'total_download', 'total_share', 'is_active', 'allow_comment',
        'comment_count', 'publish_date')
    search_fields = ('id', 'name', 'slug')
    filter_horizontal = ('widgets', )
    raw_id_fields = ('parent', 'created_by', 'last_modified_by')
    inlines = [DocumentAdminInline, PageWidgetAdminInline]


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'page', 'candidate_id', 'name', 'created_on', 'is_published',
        'message', 'is_removed', 'replied_to')
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


admin.site.register(IndexerWidget, IndexerWidgetAdmin)
admin.site.register(Widget, WidgetAdmin)
admin.site.register(Page, PageAdmin)
# admin.site.register(PageWidget, PageWidgetAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(PageCounter, PageCounterAdmin)
