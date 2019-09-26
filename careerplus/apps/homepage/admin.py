from django.contrib import admin

from .models import TopTrending, TrendingProduct, Testimonial, StaticSiteContent


class TrendingProductInline(admin.TabularInline):
    model = TrendingProduct
    list_display = ('product', 'priority', 'is_active')
    raw_id_fields = ('product', 'trendingcourse')
    extra = 1


class TopTrendingAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active', 'is_jobassistance', 'view_all', 'priority']
    search_fields = ('id', 'name')
    filter_horizontal = ('products',)
    inlines = [TrendingProductInline]


# class TrendingProductAdmin(admin.ModelAdmin):
#     list_display = ['id', 'trendingcourse', 'product', 'is_active', 'priority']
#     list_filter = ('trendingcourse', 'product')
#     search_fields = ('id', 'trendingcourse__name', 'product__name')
#     raw_id_fields = ('product', 'trendingcourse')


class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'user_name', 'rating', 'page', 'designation', 'company']
    search_fields = ('id', 'user_id', 'user_name', 'designation', 'company')


# admin.site.register(TrendingProduct, TrendingProductAdmin)
admin.site.register(TopTrending, TopTrendingAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(StaticSiteContent)


