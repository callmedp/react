# from django.contrib import admin
# from shop.models import Category, Product, ProductCategory, CategoryRelationship
# from partner.models import Vendor


# class CategoryRelationshipInline(admin.TabularInline):
#     model = CategoryRelationship
#     fk_name = 'related_from'
#     raw_id_fields = ['related_from', 'related_to']
#     extra = 1


# class CategoryProductInline(admin.TabularInline):
#     model = ProductCategory
#     fk_name = 'category'
#     raw_id_fields = ['category', 'product']
#     extra = 1


# class CategoryAdmin(admin.ModelAdmin):
#     inlines = [CategoryRelationshipInline, CategoryProductInline]


# class ProductAdmin(admin.ModelAdmin):
#     pass


# class VendorAdmin(admin.ModelAdmin):
#     pass


# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Product, ProductAdmin)
# admin.site.register(Vendor, VendorAdmin)
