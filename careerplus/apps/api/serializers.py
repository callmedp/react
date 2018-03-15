from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField
)
from order.models import Order, OrderItem
from payment.models import PaymentTxn
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
        except:
            logging.getLogger('error_log').error(" Msg= Unable to fetch Product name")

        return ''

    def get_prd_parent_id(self, obj):
        try:
            return obj.product.id
        except:
            pass
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
        except:
            pass
        return ''

    def get_variation_product_id(self, obj):
        try:
            return obj.product.id
        except:
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
        except:
            pass
        return ''

    def get_addon_product_id(self, obj):
        try:
            return obj.product.id
        except:
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
        except:
            pass
        return ''

    def get_combo_product_id(self, obj):
        try:
            return obj.product.id
        except:
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
        except:
            pass
        return ''

    def get_variation1(self, obj):
        try:
            variations = obj.order.orderitems.filter(
                parent=obj, no_process=False, is_variation=True)
            return VariationSerializer(variations, many=True).data
        except:
            pass
        return ''

    def get_addon1(self, obj):
        try:
            addons = obj.order.orderitems.filter(
                parent=obj, no_process=False, is_addon=True)
            return AddonSerializer(addons, many=True).data
        except:
            pass
        return ''

    def get_combo1(self, obj):
        try:
            combos = obj.order.orderitems.filter(
                parent=obj, no_process=False, is_combo=True)
            return ComboSerializer(combos, many=True).data
        except:
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