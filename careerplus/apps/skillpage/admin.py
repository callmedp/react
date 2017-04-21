from django.contrib import admin
from shop.models import Category, Product
from partner.models import Vendor


class ProductInline(admin.TabularInline):

    model = Category.categoryproducts.through

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'video_link', 'active')
	search_fields = ('id', 'name', 'slug')
	inlines = (
       ProductInline,
    )


class ProductAdmin(admin.ModelAdmin):
	pass

class VendorAdmin(admin.ModelAdmin):
	pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Vendor, VendorAdmin)
