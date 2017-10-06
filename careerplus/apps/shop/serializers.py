import json

from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField
)
from .models import Product
from .search_indexes import ProductIndex
from django.core.urlresolvers import reverse_lazy
from decimal import Decimal


class CRMProductSerializer(ModelSerializer):
    display_name = SerializerMethodField()
    p_class = SerializerMethodField()
    vendor_name = SerializerMethodField()
    vendor_id = SerializerMethodField()
    i_price = SerializerMethodField()
    u_price = SerializerMethodField()
    a_price = SerializerMethodField()
    g_price = SerializerMethodField()
    display_url = SerializerMethodField()
    fbt = SerializerMethodField()
    combo = SerializerMethodField()
    variation = SerializerMethodField()
    otherp = SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'display_name',
            'p_class',
            'vendor_name',
            'vendor_id',
            'display_url',
            'type_product',
            'type_flow',
            'i_price',
            'u_price',
            'a_price',
            'g_price',
            'fbt',
            'combo',
            'variation',
            'otherp',
            'active'
        ]

    def get_display_name(self,obj):
        return obj.heading

    def get_p_class(self,obj):
        return obj.product_class.slug if obj.product_class else ''

    def get_i_price(self,obj):
        return str(obj.inr_price)

    def get_u_price(self,obj):
        return str(obj.usd_price)
    
    def get_a_price(self,obj):
        return str(obj.aed_price)
    
    def get_g_price(self,obj):
        return str(obj.gbp_price)
    
    def get_vendor_name(self,obj):
        return obj.vendor.name if obj.vendor else ''

    def get_vendor_id(self,obj):
        return obj.vendor.id if obj.vendor else ''

    def get_display_url(self,obj):
        return obj.get_url(relative=True)

    def get_fbt(self, obj):
        return ProductIndex().prepare_pFBT(obj=obj)

    def get_combo(self,obj):
        return ProductIndex().prepare_pCmbs(obj=obj)

    def get_variation(self,obj):
        return ProductIndex().prepare_pVrs(obj=obj)

    def get_otherp(self,obj):
        return ProductIndex().prepare_pPOP(obj=obj)

    