from rest_framework import serializers

# app imports
from order.models import OrderItem, Order
from datetime import datetime,timedelta
from order.choices import OI_OPS_STATUS
from django.conf import settings

OI_STATUS_DICT = {
    0 : 'Unpaid',
    1 : 'Service in progress',
    4 : 'Closed',
    5 : 'Cancelled',
}

class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ('id', 'title', 'quantity', 'product', 'oi_status')

    def get_oi_status_value(self, instance):
        key = instance.oi_status
        status = ''
        if key in [161, 162, 163, 164]:
            status = instance.get_user_oi_status
        elif key in [0, 1, 4, 5]:
            status = OI_STATUS_DICT.get(key)
        return status

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

    def to_representation(self, instance):
        data = super(OrderItemSerializer, self).to_representation(instance)
        data['oi_status'] = self.get_oi_status_value(instance) if instance.oi_status else ''
        data.update({
            'name': self.get_oi_name(instance) if instance.product_id else instance.title,
            'productUrl': instance.product.get_absolute_url() if instance.product_id else '',
            'product_type_flow': instance.product.type_flow if instance.product_id else '',
            'heading': instance.product.heading if instance.product_id else '',
        })
        if self.context.get("send_course_detail", None):
            date_placed =instance.order.date_placed.strftime("%b %d, ""%Y")
            data.update({
                'img': instance.product.get_image_url(), 
                'rating': instance.product.get_ratings(),
                'avg_rating':instance.product.get_avg_ratings(),
                'price': instance.product.get_price(),
                'vendor': instance.product.vendor.name, 
                'duration':instance.product.get_duration_in_ddmmyy() if instance.product_id and instance.product.get_duration_in_day() else None,
                'enroll_date':date_placed,
                # 'remaining_days':instance.order.date_placed + timedelta(days=instance.product.get_duration_in_day())-datetime.now(),
                'status':OI_OPS_STATUS[instance.oi_status][1] if instance.oi_status else None,
                'mode':instance.product.get_studymode_db(),
                'jobs':instance.product.num_jobs,
            })
            detail = []
            max_draft_limit=settings.DRAFT_MAX_LIMIT
            if instance.oi_status == 24 and instance.draft_counter == 1 :
                 detail.append(instance.get_user_oi_status)
            elif instance.oi_status == 24 and instance.draft_counter < max_draft_limit:
                detail.append('Revised Document is ready')
            elif instance.oi_status == 24 and instance.draft_counter == max_draft_limit:
                detail.append('Final Document is ready')
            elif instance.oi_status == 181 :
                detail.append('Waiting For Input')
            data.update({'view_details':{date_placed:detail}})

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
        data['status'] = instance.get_status if instance.status in [0, 1, 3, 5] else ''
        data.update({
            'canCancel': True if instance.status == 0 else False,
            'downloadInvoice': True if instance.status in [1, 3] else False
        })
        return data
