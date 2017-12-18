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
        ]


class OrderItemDetailSerializer(ModelSerializer):
    product = SerializerMethodField('get_product1')
    # variation = SerializerMethodField('get_variation1')
    # variation_name = SerializerMethodField('get_variation_name')
    # parent = SerializerMethodField('get_parent')
    # addon = SerializerMethodField('get_addon')
    # addon_name = SerializerMethodField('get_addon_name')
    # combo = SerializerMethodField('get_combo')
    # combo_name = SerializerMethodField('get_combo_name')

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'cost_price',
            'product',
            'parent',
            'is_variation',
            'is_addon',
            'is_combo',
            # 'variation_name',
            # 'addon_name',
            # 'combo_name',
            # 'units',
        ]

    def get_product1(self, obj):
        try:
            return obj.product.pk
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
            'payment_date',
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
