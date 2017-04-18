from django.contrib import admin
from . import models


class CategoryRelationshipInline(admin.TabularInline):
    model = models.CategoryRelationship
    fk_name = 'related_from'
    raw_id_fields = ['related_from', 'related_to']
    extra = 1


class CategoryProductInline(admin.TabularInline):
    model = models.ProductCategory
    fk_name = 'category'
    raw_id_fields = ['category', 'product']
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryRelationshipInline, CategoryProductInline]


class AttributeInline(admin.TabularInline):
    model = models.ProductAttribute
    raw_id_fields = ['attribute', 'product']
    extra = 1


class RelatedProductInline(admin.TabularInline):
    model = models.RelatedProduct
    fk_name = 'primary'
    raw_id_fields = ['primary', 'secondary']
    extra = 1


class ChildProductInline(admin.TabularInline):
    model = models.ChildProduct
    fk_name = 'father'
    raw_id_fields = ['father', 'children']
    extra = 1


class CategoryInline(admin.TabularInline):
    model = models.ProductCategory
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [AttributeInline, CategoryInline, RelatedProductInline, ChildProductInline]
    prepopulated_fields = {"slug": ("name",)}
    
#     def get_queryset(self, request):
#         qs = super(ProductAdmin, self).get_queryset(request)
#         return (
#             qs
#             .select_related('product_class', 'parent')
#             .prefetch_related(
#                 'attribute_values',
#                 'attribute_values__attribute'))





class ProductExtraInfoAdmin(admin.ModelAdmin):
    list_display = ['info_type', 'product', 'content_object']


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Attribute)
admin.site.register(models.Keyword)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Currency)
admin.site.register(models.ProductExtraInfo, ProductExtraInfoAdmin)


