# DRF Import
from rest_framework import serializers
from django.conf import settings

# Inter-App Import
from homepage.models import StaticSiteContent
from order.models import Order ,OrderItem
from shop.models import ProductSkill,ProductCategory, Product,Category
# from api.serializers import OrderItemDetailSerializer
from shared.rest_addons.mixins import SerializerFieldsMixin
from django.conf import settings


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
    get_user_oi_status = serializers.SerializerMethodField()
    auto_upload = serializers.SerializerMethodField()
    oi_resume = serializers.SerializerMethodField()
    oio_linkedin =serializers.SerializerMethodField()
    oi_draft = serializers.SerializerMethodField()
    service_resume_upload_shine = serializers.SerializerMethodField()
    product_is_pause_service = serializers.SerializerMethodField()
    service_pause_status = serializers.SerializerMethodField()
    is_assigned = serializers.SerializerMethodField()
    updated_from_trial_to_regular = serializers.ReadOnlyField()
    neo_mail_sent = serializers.ReadOnlyField()
    product_vendor = serializers.SerializerMethodField()
    product_sub_type_flow = serializers.SerializerMethodField()


    
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


    def get_is_assigned(self,obj):
        return obj.is_assigned()

    def get_service_pause_status(self,obj):
        return obj.service_pause_status()

    def get_oi_draft(self,obj):
        return obj.oi_draft.name if obj.oi_draft else ''

    def get_oi_resume(self,obj):
        return obj.oi_resume.name if obj.oi_resume else ''

    def get_product_is_pause_service(self,obj):
        return obj.product.is_pause_service if obj.product_id else ''

    def get_oio_linkedin(self,obj):
        return obj.oio_linkedin_id if obj.oio_linkedin else ''

    def get_auto_upload(self,obj):
        return obj.order.auto_upload

    def get_service_resume_upload_shine(self,obj):
        return obj.order.service_resume_upload_shine


    def get_get_user_oi_status(self,obj):
        return obj.get_user_oi_status   

    def get_get_exp_db(self,obj):
        return obj.product.get_exp_db() if obj.product else ''

    def get_days_left_oi_product(self,obj):
        return obj.days_left_oi_product

    def get_new_oi_status(self,obj):
        return obj.get_oi_status

    # def get_product_name(self,obj):
    #     return obj.product_name

    def get_product_vendor(self,obj):
        return obj.product.vendor.slug if obj.product and obj.product.vendor else ''

    def get_product_type_flow(self,obj):
        return obj.product.type_flow if obj.product else ''


    def get_product_sub_type_flow(self,obj):
        return obj.product.sub_type_flow if obj.product else ''



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
        request = self.context.get('request', {})
        query_dict = getattr(request, 'GET', {})
        select_type = query_dict.get('select_type',0)
        orderitems = obj.orderitems.filter(parent=None)
        if select_type == 1:
            orderitems = orderitems.exclude(oi_status=4)
        elif select_type == 2:
            orderitems = orderitems.filter(oi_status=4)

        return OrderItemDetailSerializer(orderitems, many=True).data


class DashboardCancellationSerializer(serializers.Serializer):
    candidate_id = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    order_id = serializers.IntegerField(required=True)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product 
        fields = ["avg_rating","inr_price","id", "heading", "name",]
    
    def to_representation(self, instance):
        data = super(ProductSerializer, self).to_representation(instance)
        data['mode']=instance.get_studymode_db()
        data['duration']=instance.get_duration_in_day()
        data['url']=instance.get_url()
        data['image_url']=instance.get_image_url()
        data['rating']=instance.get_ratings()
        data['price'] =instance.get_price()
        data['vendor']=instance.get_vendor()
        return data
   
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name",]
class RecentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id']
