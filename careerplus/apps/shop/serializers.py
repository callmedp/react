import json

from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField
)
from .models import Product
from .search_indexes import ProductIndex
from django.urls import reverse,reverse_lazy
from decimal import Decimal
from search.templatetags.search_tags import get_choice_display           

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
    attributes = SerializerMethodField()
    delivery_type = SerializerMethodField()

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
            'attributes',
            'active',
            'delivery_type',
            'short_description',
            'visible_on_crm'
        ]

    def get_display_name(self,obj):
        return obj.heading

    def get_p_class(self,obj):
        return obj.product_class.slug if obj.product_class else ''

    def get_i_price(self,obj):
        if obj.type_product == 1 and obj.is_course:
            return 0.0    
        return float(obj.inr_price)

    def get_u_price(self,obj):
        if obj.type_product == 1 and obj.is_course:
            return 0.0    
        return float(obj.usd_price)
    
    def get_a_price(self,obj):
        if obj.type_product == 1 and obj.is_course:
            return 0.0    
        return float(obj.aed_price)
    
    def get_g_price(self,obj):
        if obj.type_product == 1 and obj.is_course:
            return 0.0    
        return float(obj.gbp_price)
    
    def get_vendor_name(self,obj):
        return obj.vendor.name if obj.vendor else ''

    def get_vendor_id(self,obj):
        return obj.vendor.id if obj.vendor else ''

    def get_display_url(self,obj):
        return obj.get_url(relative=False)

    def get_fbt(self, obj):
        return ProductIndex().prepare_pFBT(obj=obj)

    def get_combo(self,obj):
        return ProductIndex().prepare_pCmbs(obj=obj)

    def get_delivery_type(self, obj):
        delivery_types = obj.get_delivery_types()
        if delivery_types.exists():
            keys = ['name', 'slug', 'inr_price', 'usd_price', 'aed_price', 'gbp_price']
            delivery_list = []

            for dt in delivery_types:
                dt_dict = {}
                [dt_dict.update({key: str(getattr(dt, key))}) for key in keys]
                delivery_list.append(dt_dict)

            return json.dumps(delivery_list)
        return []

    def get_variation(self,obj):
        var_dict = {
            'variation': False,
            'var_list': []
        }
        var_list = []
        if obj.type_product == 1:
            var  = obj.get_variations()
            if var:
                if obj.is_course:
                    var_dict.update({
                        'variation': True
                    })
                    for pv in var:
                        attr = ''
                        mode = get_choice_display(pv.get_studymode(), "STUDY_MODE")
                        duration = get_choice_display(pv.get_duration(), "DURATION_DICT")
                        certify = 'Yes' if pv.get_cert() else 'No'
                        if mode:
                            attr = 'Mode:{} | '.format(mode)
                        if duration:
                            attr += ' Duration:{} | '.format(duration)
                        if certify:
                            attr += ' Certification:{} '.format(certify)
                        var_list.append({
                            'id': pv.id,
                            'label': pv.name,
                            'attr': attr,
                            'inr_price': float(pv.inr_price),
                            'usd_price': float(pv.usd_price),
                            'aed_price': float(pv.aed_price),
                            'gbp_price': float(pv.gbp_price),
                            'short_description': pv.short_description,
                            'visible_on_crm': pv.visible_on_crm
                        })
                    var_dict.update({
                        'var_list': var_list
                    })
                elif obj.is_writing or obj.is_service:
                    var_dict.update({
                        'variation': True
                    })
                    for pv in var:
                        attr = ''
                        experience = get_choice_display(pv.get_exp(), "EXP_DICT")
                        if experience:
                            attr = 'Exp: {} '.format(experience)
                        var_list.append({
                            'id': pv.id,
                            'label': pv.name,
                            'attr': attr,
                            'inr_price': float(pv.inr_price),
                            'usd_price': float(pv.usd_price),
                            'aed_price': float(pv.aed_price),
                            'gbp_price': float(pv.gbp_price),
                            'short_description': pv.short_description,
                            'visible_on_crm': pv.visible_on_crm
                        })
                var_dict.update({
                    'var_list': var_list
                })
            return json.dumps(var_dict)
        else:
            return json.dumps(var_dict)     
        
    def get_attributes(self,obj):
        attr = ''
        if obj.type_product in [0,1,3,4,5]:
            if obj.is_course:
                mode = get_choice_display(obj.get_studymode(), "STUDY_MODE")
                duration = get_choice_display(obj.get_duration(), "DURATION_DICT")
                certify = 'Yes' if obj.get_cert() else 'No'
                if mode:
                    attr = 'Mode:{} | '.format(mode)
                if duration:
                    attr += ' Duration:{} | '.format(duration)
                if certify:
                    attr += ' Certification:{} '.format(certify)
            elif obj.is_writing or obj.is_service:
                experience = get_choice_display(obj.get_exp(), "EXP_DICT")
                if experience:
                    attr = 'Exp: {} '.format(experience)
        return attr