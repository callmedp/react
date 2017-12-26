from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField
)
from order.models import Order, OrderItem
from payment.models import PaymentTxn


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = PaymentTxn
        fields = [
            'txn',
            'payment_mode',
            'payment_date',
        ]


class VariationSerializer(ModelSerializer):
    variation_name = SerializerMethodField('get_variation_prd1')

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'variation_name',
            'quantity',  # unit as quantity
            'selling_price',  # price as selling_price
        ]

    def get_variation_prd1(self, obj):
        try:
            return obj.product.name
        except:
            pass
        return ''


class AddonSerializer(ModelSerializer):
    addon_name = SerializerMethodField('get_addon_prd1')

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'addon_name',
            'quantity',
            'selling_price'
        ]

    def get_addon_prd1(self, obj):
        try:
            return obj.product.name
        except:
            pass
        return ''


class ComboSerializer(ModelSerializer):
    combo_name = SerializerMethodField('get_combo_prd1')

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'combo_name',
            'quantity',
            'selling_price'
        ]

    def get_combo_prd1(self, obj):
        try:
            return obj.product.name
        except:
            pass
        return ''


class OrderItemDetailSerializer(ModelSerializer):
    product = SerializerMethodField('get_product1')
    variation = SerializerMethodField('get_variation1')
    addon = SerializerMethodField('get_addon1')
    combo = SerializerMethodField('get_combo1')

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'cost_price',
            'product',
            'quantity',
            'selling_price',
            'parent',
            'variation',
            'addon',
            'combo',
        ]

    def get_product1(self, obj):
        try:
            return obj.product.name
        except:
            pass
        return ''

    def get_variation1(self, obj):
        try:
            parent_ois = obj.order.orderitems.filter(parent=None)
            for parent_oi in parent_ois:
                variations = obj.order.orderitems.filter(parent=parent_oi, is_variation=True)
                return VariationSerializer(variations, many=True).data
        except:
            pass
        return ''

    def get_addon1(self, obj):
        try:
            parent_ois = obj.order.orderitems.filter(parent=None)
            for parent_oi in parent_ois:
                addons = obj.order.orderitems.filter(parent=parent_oi, is_addon=True)
                return AddonSerializer(addons, many=True).data
        except:
            pass
        return ''

    def get_combo1(self, obj):
        try:
            parent_ois = obj.order.orderitems.filter(parent=None)
            for parent_oi in parent_ois:
                combos = obj.order.orderitems.filter(parent=parent_oi, is_combo=True)
                return ComboSerializer(combos, many=True).data
        except:
            pass
        return ''


class OrderListHistorySerializer(ModelSerializer):
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

    def get_orderitems1(self, obj):
        orderitems = obj.orderitems.all()
        if orderitems:
            return OrderItemDetailSerializer(orderitems, many=True).data

    def get_txn(self, obj):
        payment_obj = obj.ordertxns.all()
        if payment_obj:
            return PaymentSerializer(payment_obj, many=True).data
