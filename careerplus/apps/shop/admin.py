from django.contrib import admin
from . import models
from core.api_mixin import ShineProfileDataUpdate
from django.contrib import messages

class CategoryRelationshipInline(admin.StackedInline):
    model = models.CategoryRelationship
    fk_name = 'related_from'
    readonly_fields = ('modified',)
    raw_id_fields = ['related_from', 'related_to']
    extra = 1


class CategoryProductInline(admin.TabularInline):
    model = models.ProductCategory
    fk_name = 'category'
    readonly_fields = ('modified',)
    raw_id_fields = ['category', 'product']
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryRelationshipInline, CategoryProductInline]
    readonly_fields = ('modified',)
    list_display = [
        'name', 'modified', 'type_level']
    search_fields = ('name',)
    list_filter = ('type_level', )


class AttributeAdmin(admin.ModelAdmin):
    readonly_fields = ('modified',)
    list_display = [
        'name', 'display_name',]
    search_fields = ('name',)
    raw_id_fields = ('product_class', 'option_group')

class AttributeInline(admin.TabularInline):
    model = models.ProductAttribute
    raw_id_fields = ['attribute', 'product']
    fk_name = 'product'
    exclude = ('value_ltext',)
    extra = 1


class FAQuestionInline(admin.TabularInline):
    model = models.FAQProduct
    raw_id_fields = ['question', 'product']
    fk_name = 'product'
    extra = 1


class RelatedProductInline(admin.TabularInline):
    model = models.RelatedProduct
    fk_name = 'primary'
    raw_id_fields = ['primary', 'secondary']
    extra = 1


class VariationProductInline(admin.TabularInline):
    model = models.VariationProduct
    fk_name = 'main'
    raw_id_fields = ['main', 'sibling']
    extra = 1


class OptionInline(admin.TabularInline):
    model = models.AttributeOption
    fk_name = 'group'
    raw_id_fields = ['group']
    extra = 1


class OptionGroupAdmin(admin.ModelAdmin):
    inlines = [OptionInline]


class ChildProductInline(admin.TabularInline):
    model = models.ChildProduct
    fk_name = 'father'
    raw_id_fields = ['father', 'children']
    extra = 1


class CategoryInline(admin.TabularInline):
    model = models.ProductCategory
    fk_name = 'product'
    extra = 1

class ProductExtraInfoInline(admin.TabularInline):
    model = models.ProductExtraInfo
    fk_name = 'product'
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    inlines = [CategoryInline, RelatedProductInline, ChildProductInline, VariationProductInline,
        FAQuestionInline, AttributeInline, ProductExtraInfoInline]
    prepopulated_fields = {"slug": ("name",)}

# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name']
#     inlines = [CategoryInline, RelatedProductInline, ChildProductInline, VariationProductInline,
#         FAQuestionInline, AttributeInline, ]
#     prepopulated_fields = {"slug": ("name",)}
    
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


class DeliveryServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'active', 'inr_price', 'usd_price', 'aed_price', 'gbp_price']


class ShineProfileDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type_flow', 'sub_type_flow', 'priority_value', 'vendor']

    def save_model(self, request, obj, form, change):
        resp = ShineProfileDataUpdate().update_shine_profile_data()
        if resp:
            messages.add_message(request, messages.SUCCESS, 'Shine Profile flow data updated on Shine.')
        super(ShineProfileDataAdmin, self).save_model(request, obj, form, change)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class SkillAdmin(admin.ModelAdmin):
    search_fields = ('name',)


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Attribute, AttributeAdmin)
admin.site.register(models.Keyword)
admin.site.register(models.SubCategory)
admin.site.register(models.ProductClass)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.AttributeOptionGroup, OptionGroupAdmin)
admin.site.register(models.DeliveryService, DeliveryServiceAdmin)
admin.site.register(models.ShineProfileData, ShineProfileDataAdmin)
admin.site.register(models.Skill, SkillAdmin)
# admin.site.register(models.ProductExtraInfo, ProductExtraInfoAdmin)
