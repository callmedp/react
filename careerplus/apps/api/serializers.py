from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    Serializer
)
from django.conf import settings
from rest_framework import serializers

from order.models import Order, OrderItem
from shop.models import Product, ShineProfileData
from payment.models import PaymentTxn
from partner.models import Certificate, Vendor

import logging


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = PaymentTxn
        fields = [
            'txn',
            'payment_mode',
            'payment_date',
        ]


class ParentSerializer(ModelSerializer):
    productname = SerializerMethodField('get_product_name')
    productid = SerializerMethodField('get_prd_parent_id')

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'productname',
            'productid',
            'quantity',  # unit as quantity
            'selling_price',  # price as selling_price
        ]

    def get_product_name(self, obj):
        try:
            return obj.product.name
        except Exception as e:
            logging.getLogger('error_log').error("Unable to return Product name %s"% str(e))
        return ''

    def get_prd_parent_id(self, obj):
        try:
            return obj.product.id
        except Exception as e:
            logging.getLogger('error_log').error("Unable to return product parent id %s" % str(e))
        return ''


class VariationSerializer(ModelSerializer):
    variation_name = SerializerMethodField('get_variation_product_name')
    productid = SerializerMethodField('get_variation_product_id')

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'parent',
            'variation_name',
            'productid',
            'quantity',  # unit as quantity
            'selling_price',  # price as selling_price
        ]

    def get_variation_product_name(self, obj):
        try:
            return obj.product.name
        except Exception as e:
            logging.getLogger('error_log').error(" Msg= Unable to return variant Product name %s"% str(e))
            pass
        return ''

    def get_variation_product_id(self, obj):
        try:
            return obj.product.id
        except Exception as e:
            logging.getLogger('error_log').error("Unable to get variant Product id  %s"% str(e))
            pass
        return ''


class AddonSerializer(ModelSerializer):
    addon_name = SerializerMethodField('get_addon_product_name')
    productid = SerializerMethodField('get_addon_product_id')

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'parent',
            'addon_name',
            'productid',
            'quantity',
            'selling_price'
        ]

    def get_addon_product_name(self, obj):
        try:
            return obj.product.name
        except Exception as e:
            logging.getLogger('error_log').error("Unable to return addon Product name %s"% str(e))
            pass
        return ''

    def get_addon_product_id(self, obj):
        try:
            return obj.product.id
        except Exception as e:
            logging.getLogger('error_log').error("Unable to return addon Product id %s"% str(e))
            pass
        return ''


class ComboSerializer(ModelSerializer):
    combo_name = SerializerMethodField('get_combo_product_name')
    productid = SerializerMethodField('get_combo_product_id')

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'parent',
            'combo_name',
            'productid',
            'quantity',
            'selling_price'
        ]

    def get_combo_product_name(self, obj):
        try:
            return obj.product.name
        except Exception as e:
            logging.getLogger('error_log').error("Unable to return combo Product name %s"% str(e))
            pass
        return ''

    def get_combo_product_id(self, obj):
        try:
            return obj.product.id
        except Exception as e:
            logging.getLogger('error_log').error("Unable to return combo Product id %s"% str(e))
            pass
        return ''


class OrderItemDetailSerializer(ModelSerializer):
    prdid = SerializerMethodField('get_parentprdid')
    parent = SerializerMethodField('get_parent1')
    variation = SerializerMethodField('get_variation1')
    addon = SerializerMethodField('get_addon1')
    combo = SerializerMethodField('get_combo1')

    class Meta:
        model = OrderItem
        fields = [
            'prdid',
            'parent',
            'variation',
            'addon',
            'combo',
        ]

    def get_parentprdid(self, obj):
        return obj.product.id

    def get_parent1(self, obj):
        try:
            v = obj.order.orderitems.filter(parent=None)
            return ParentSerializer(v, many=True).data
        except Exception as e:
            logging.getLogger('error_log').error("Unable to return order item parent %s"% str(e))
            pass
        return ''

    def get_variation1(self, obj):
        try:
            variations = obj.order.orderitems.filter(
                parent=obj, no_process=False, is_variation=True)
            return VariationSerializer(variations, many=True).data
        except Exception as e:
            logging.getLogger('error_log').error("Unable to return variat order item  %s"% str(e))
            pass
        return ''

    def get_addon1(self, obj):
        try:
            addons = obj.order.orderitems.filter(
                parent=obj, no_process=False, is_addon=True)
            return AddonSerializer(addons, many=True).data
        except Exception as e:
            logging.getLogger('error_log').error("Unable to return addon order item %s"% str(e))
            pass
        return ''

    def get_combo1(self, obj):
        try:
            combos = obj.order.orderitems.filter(
                parent=obj, no_process=False, is_combo=True)
            return ComboSerializer(combos, many=True).data
        except Exception as e:
            logging.getLogger('error_log').error("Unable to return combo order item %s"% str(e))
            pass
        return ''


class OrderListHistorySerializer(ModelSerializer):
    status = SerializerMethodField('get_order_status')
    orderitems = SerializerMethodField('get_orderitems1')
    transaction_id = SerializerMethodField('get_txn')

    class Meta:
        model = Order
        fields = [
            'id',
            'candidate_id',
            'first_name',
            'email',
            'mobile',
            'currency',
            'created',
            'status',
            'transaction_id',
            'crm_sales_id',
            'total_incl_tax',
            'total_excl_tax',
            'orderitems',
        ]

    def get_order_status(self, obj):
        if obj.status == 1:
            return 'Paid'
        elif obj.status == 2:
            return "InProcess"
        elif obj.status == 3:
            return "Closed"

    def get_orderitems1(self, obj):
        orderitems = obj.orderitems.filter(parent=None)
        if orderitems:
            return OrderItemDetailSerializer(orderitems, many=True).data

    def get_txn(self, obj):
        payment_obj = obj.ordertxns.all()
        if payment_obj:
            return PaymentSerializer(payment_obj, many=True).data


class RecommendedProductSerializer(ModelSerializer):
    display_name = SerializerMethodField()
    pUrl = SerializerMethodField()
    pImg = SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'display_name',
            'pUrl',
            'avg_rating',
            'no_review',
            'buy_count',
            'num_jobs',
            'pImg',
        ]

    def get_display_name(self, obj):
        return obj.get_name

    def get_pUrl(self, obj):
        return obj.get_url(relative=False) if obj.get_url(relative=False) else ''

    def get_pImg(self, obj):
        return obj.get_image_url(relative=False)


class RecommendedProductSerializerSolr(Serializer):
    id = serializers.CharField()
    display_name = serializers.CharField(source='pHd')
    buy_count = serializers.IntegerField(source='pBC')
    pImg = serializers.CharField()
    pURL = serializers.CharField()
    pStar = serializers.ListField(
        child=serializers.CharField())
    no_jobs = serializers.IntegerField(source='pNJ')
    review_count = serializers.IntegerField(source='pRC')
    avg_rating = serializers.DecimalField(
        source='pARx',
        max_digits=8, decimal_places=2)
    # pSkilln = serializers.ListField(
    #     child=serializers.CharField())

class  ShineDataFlowDataSerializer(ModelSerializer):

    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ShineProfileData
        fields = ('id', 'name', 'image_url', 'priority_value')

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url


class CertificateSerializer(ModelSerializer):
    skill = serializers.SerializerMethodField()

    class Meta:
        model = Certificate
        fields = ('id', 'name', 'skill', 'vendor_certificate_id', 'vendor_provider')


    def get_skill(self, obj):
        if obj.skill:
            k = list(map(lambda x: x.lower(), obj.skill.split(',')))
            return k

class VendorCertificateSerializer(ModelSerializer):
    certificate_set = CertificateSerializer(many=True, read_only=True)

    class Meta:
        model = Vendor
        fields = ("name", "certificate_set")

    def to_representation(self, obj):
        response = super(VendorCertificateSerializer, self).to_representation(obj)
        if response['certificate_set']:
            return {
                response['name']: response['certificate_set']
            }


class ImportCertificateSerializer(Serializer):

    class Meta:
        fields = (
            'name', 'skill', 'vendor_certificate_id', 'active_from',
            'expiry', 'licenseNumber'
        )

    def __init__(self, *args, **kwargs):
        super(ImportCertificateSerializer, self).__init__(*args, **kwargs)
        context = kwargs.get('context', None)
        if context:
            self.vendor_provider = context.get('vendor_provider', None)

    name = serializers.CharField()
    skill = serializers.CharField()
    vendor_certificate_id = serializers.CharField()
    active_from = serializers.CharField()
    expiry = serializers.CharField()
    licenseNumber = serializers.CharField()
    vendor_provider = serializers.SerializerMethodField()
    overallScore = serializers.CharField()

    def get_vendor_provider(self, obj):
        return self.vendor_provider


