from rest_framework import serializers
from homepage.models import StaticSiteContent
from order.models import Order ,OrderItem
# from api.serializers import OrderItemDetailSerializer
from shared.rest_addons.mixins import SerializerFieldsMixin

class StaticSiteContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = StaticSiteContent
        fields = ['page_type','content','page_name']


class OrderItemDetailSerializer(SerializerFieldsMixin,serializers.ModelSerializer):
    new_oi_status = serializers.SerializerMethodField()
    # product_name = serializers.SerializerMethodField()
    product_type_flow = serializers.SerializerMethodField()
    days_left_oi_product = serializers.SerializerMethodField()
    get_exp_db = serializers.SerializerMethodField()
    # order = serializers.SerializerMethodField('get_order')
    # prdid = serializers.SerializerMethodField('get_parentprdid')
    # parent = SerializerMethodField('get_parent1')
    # variation = SerializerMethodField('get_variation1')
    # addon = SerializerMethodField('get_addon1')
    # combo = SerializerMethodField('get_combo1')

    class Meta:
        model = OrderItem
        exclude = ('assigned_to','assigned_by','oi_price_before_discounts_incl_tax',
                   'oi_price_before_discounts_excl_tax','quantity','upc','archive_json','coi_id',
                   'delivery_price_excl_tax','delivery_price_incl_tax','cost_price','tax_amount','tat_date',
                   'expiry_date','wc_cat','wc_sub_cat','wc_status','wc_follow_up','partner')

    #

    def get_get_exp_db(self,obj):
        return obj.product.get_exp_db() if obj.product else ''

    def get_days_left_oi_product(self,obj):
        return obj.days_left_oi_product

    def get_new_oi_status(self,obj):
        return obj.get_oi_status

    # def get_product_name(self,obj):
    #     return obj.product_name

    def get_product_type_flow(self,obj):
        return obj.product.type_flow if obj.product else ''



class OrderListSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField('get_order_status')
    orderitems = serializers.SerializerMethodField('get_orderitems1')

    class Meta:
        model = Order
        fields = [
            'id',
            'candidate_id',
            'first_name',
            'email',
            'mobile',
            'created',
            'status',
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
        request = self.context.get('request',{})
        query_dict = getattr(request,'GET',{})
        select_type = query_dict.get('select_type',0)
        orderitems = obj.orderitems.filter(parent=None)
        if select_type == 1:
            orderitems = orderitems.exclude(oi_status=4)
        elif select_type == 2:
            orderitems = orderitems.filter(oi_status=4)

        return OrderItemDetailSerializer(orderitems, many=True).data




