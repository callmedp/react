from django.contrib import admin

from .models import TopTrending, TrendingProduct


class TopTrendingAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'is_active', 'is_jobassistance', 'view_all', 'priority']
	search_fields = ('id', 'name')


class TrendingProductAdmin(admin.ModelAdmin):
	list_display = ['id', 'trendingcourse', 'product', 'is_active', 'priority']
	list_filter = ('trendingcourse', 'product')
	search_fields = ('id', 'trendingcourse__name', 'product__name')


admin.site.register(TrendingProduct, TrendingProductAdmin)
admin.site.register(TopTrending, TopTrendingAdmin)
