from rest_framework import serializers

# app imports
from order.models import OrderItem, Order
from datetime import datetime,timedelta
from order.choices import OI_OPS_STATUS
from django.conf import settings
import pytz
from django.urls import reverse
from review.models import Review
from .helpers import get_courses_detail

OI_STATUS_DICT = {
    0: 'Unpaid',
    1: 'Service in progress',
    4: 'Closed',
    5: 'Cancelled',
}

OI_OPS_STATUS_dict=dict(OI_OPS_STATUS)
class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ('id', 'title', 'quantity', 'product', 'oi_status')

    def get_oi_status_value(self, instance):
        key = instance.oi_status
        order_key = instance.order.status
        status = ''
        if key == 4:
            status = 'Closed'
        elif key in [161, 162, 163, 164]:
            status = instance.get_user_oi_status
        elif order_key in [0, 1, 5]:
            status = OI_STATUS_DICT.get(order_key)
        return status
    # def get_product_is_pause_service(self,obj):
    #     return obj.product.is_pause_service if obj.product_id else ''

    def get_oi_name(self, instance):
        prd = instance.product
        name = prd.get_name
        exp_db = prd.get_exp_db()
        studymode = prd.get_studymode_db()
        coursetype = prd.get_coursetype_db()
        duration = prd.get_duration_in_ddmmyy()

        if exp_db:
            name += ' - ' + exp_db
        if studymode:
            name += ' - ' + studymode
        if coursetype:
            name += ' - ' + coursetype
        if duration:
            name += ' - ' + duration
        return name
    

    def convert_to_month(self,duration):
        months = duration//30
        days = duration%30
        if months >1:
            month_str = "months"
        else: 
            month_str = "month"
        if days >1:
            days_str = "days"
        else:
            days_str = "day"
        if months ==0:
            return str(days)+" day"
        elif days ==0:
            return str(months)
        elif months ==0 and days==0:
            return 0+" day" 
        return str(months)+" "+month_str+" "+str(days)+" "+days_str
    
    def get_remaining_days(self,instance):
        remaining_days = 0
        if instance.product.get_duration_in_day():
            rem_days = ((instance.order.date_placed + timedelta(days=instance.product.get_duration_in_day()))-datetime.now(pytz.utc)).days
            remaining_days = rem_days if rem_days > 0 else 0
        return remaining_days
    
    def service_pause_status(self,instance):
        pause_resume_ops_count = instance.orderitemoperation_set.filter(oi_status__in=[
                                                                    34, 35]).count()
        if pause_resume_ops_count & 1 and instance.oi_status == 34:
            return False
        return True
    
    def get_product_is_pause_service(self,obj):
        return obj.product.is_pause_service if obj.product_id else ''


    def to_representation(self, instance):
        data = super(OrderItemSerializer, self).to_representation(instance)
        data['oi_status'] = self.get_oi_status_value(instance) if instance.oi_status else ''
        data.update({
            'name': self.get_oi_name(instance) if instance.product_id else instance.title,
            'productUrl': instance.product.get_absolute_url() if instance.product_id else '',
            'product_type_flow': instance.product.type_flow if instance.product_id else '',
            'heading': instance.product.heading if instance.product_id else '',
        })
        if self.context.get("get_details", None):
            date_placed =instance.order.date_placed.strftime("%d %b %Y")
            data.update({
                'img': instance.product.get_image_url(), 
                'rating': instance.product.get_ratings(),
                'avg_rating':instance.product.get_avg_ratings(),
                'price': instance.product.get_price(),
                'vendor': instance.product.vendor.name, 
                'duration' : self.convert_to_month(int(instance.product.get_duration_in_day())) if instance.product_id and instance.product.get_duration_in_day() else None,
                'enroll_date': date_placed,
                'remaining_days': self.get_remaining_days(instance),
                'no_review':instance.product.no_review,
                'new_oi_status':OI_OPS_STATUS_dict.get(instance.oi_status) if instance.oi_status else None,
                'mode':instance.product.get_studymode_db(),
                'oi_status':instance.oi_status if instance.oi_status else None,
                'jobs':instance.product.num_jobs,
                'no_of_comments':instance.message_set.filter(is_internal=False).count(),
                'service_pause_status':self.service_pause_status(instance),
                'get_product_is_pause_service':self.get_product_is_pause_service(instance),
                'duration_in_days': int(instance.product.get_duration_in_day()) if instance.product_id and instance.product.get_duration_in_day() else '',
            })
            course_detail = get_courses_detail(instance)
            data.update({
                'date_created':course_detail['date_created'],
                'datalist':course_detail['datalist'],
                'options':course_detail['options']
                })
        return data

class OrderSerializer(serializers.ModelSerializer):
    """
        Serializer for `Order` model
    """

    order_status = serializers.ReadOnlyField(source='get_status')
    class Meta:
        model = Order
        exclude = ('co_id', 'archive_json', 'site', 'assigned_to', 'wc_cat', 'wc_sub_cat', 'wc_status',
            'wc_follow_up', 'welcome_call_done', 'welcome_call_records', 'midout_sent_on', 'paid_by', 'invoice',
            'crm_sales_id', 'crm_lead_id', 'sales_user_info', 'auto_upload', 'created', 'modified')

    def to_representation(self, instance):
        data = super(OrderSerializer, self).to_representation(instance)
        data['date_placed'] = instance.date_placed.date().strftime('%d %b %Y') if instance.date_placed else None
        data['currency'] = instance.get_currency()
        data['status'] = self.get_order_status(instance) if instance.status in [0, 1, 3, 5] else ''
        data.update({
            'canCancel': True if instance.status == 0 else False,
            'downloadInvoice': True if instance.status in [1, 3] else False
        })
        return data

    def get_order_status(self, instance):
        if instance.status == 1:
            return 'Open'
        return instance.get_status

class ReviewSerializer(serializers.ModelSerializer):
    """
    Review serializer
    """
    class Meta:
        model = Review
        fields = ('__all__' )
    
    def to_representation(self, instance):
        data = super(ReviewSerializer, self).to_representation(instance)
        data['rating'] = instance.get_ratings()
        data['created'] = instance.created.date().strftime('%d %b %Y')
        data['modified'] = instance.modified.date().strftime('%d %b %Y') if instance.modified else None
        return data