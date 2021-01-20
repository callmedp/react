from rest_framework import serializers

# app imports
from order.models import OrderItem, Order
from datetime import datetime,timedelta
from order.choices import OI_OPS_STATUS
from django.conf import settings

OI_STATUS_DICT = {
    0: 'Unpaid',
    1: 'Service in progress',
    4: 'Closed',
    5: 'Cancelled',
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
    
    def get_courses_detail(self,instance):
        detail = []
        max_draft_limit=settings.DRAFT_MAX_LIMIT

        if instance.product.type_flow in [1, 12, 13]:
            ops = instance.orderitemoperation_set.filter(oi_status__in=[2, 5, 24, 26, 27, 161, 162, 163, 164, 181])
        elif instance.product.vendor.slug == 'neo':
            ops = instance.orderitemoperation_set.filter(oi_status__in=[5, 33, 4, 161, 162, 163, 164])
        elif instance.product.type_flow in [2, 14]:
            ops = instance.orderitemoperation_set.filter(oi_status__in=[5, 6, 161, 162, 163, 164])
        elif instance.product.type_flow == 3:
            ops = instance.orderitemoperation_set.filter(oi_status__in=[2, 5, 121, 161, 162, 163, 164])
        elif instance.product.type_flow == 4:
            ops = instance.orderitemoperation_set.filter(oi_status__in=[2, 5, 6, 61, 161, 162, 163, 164])
        elif instance.product.type_flow == 5:
            ops = instance.orderitemoperation_set.filter(oi_status__in=[2, 5, 6, 36, 37, 61, 161, 162, 163, 164])
        elif instance.product.type_flow == 6:
            ops = instance.oi.orderitemoperation_set.filter(oi_status__in=[6, 81, 82, 161, 162, 163, 164])
        elif instance.product.type_flow in [7, 15]:
            ops = instance.orderitemoperation_set.filter(oi_status__in=[2, 4, 5, 6, 61, 161, 162, 163, 164])
        elif instance.product.type_flow == 8:
            oi_status_list = [2, 49, 5, 46, 48, 27, 4, 161, 162, 163, 181, 164]
            ops = instance.orderitemoperation_set.filter(oi_status__in=oi_status_list)
        elif instance.product.type_flow == 10:
            ops = instance.orderitemoperation_set.filter(oi_status__in=[5, 6, 101, 161, 162, 163, 164])
        elif instance.product.type_flow == 16:
            ops = instance.orderitemoperation_set.filter(oi_status__in=[5, 6, 4])
        
        datalist = []
        options = []
        oi = instance
        date_created = ''
        
        if oi.product.type_flow == 1 or  oi.product.type_flow == 12 or oi.product.type_flow == 13:
            for op in ops:
                date_created =op.created
                if op.oi_status == 24 and op.draft_counter == 1:
                    datalist.append(op.get_user_oi_status)
                elif op.oi_status == 24 and op.draft_counter < max_draft_limit:
                    datalist.append('Revised Document is ready')
                elif op.oi_status == 24 and op.draft_counter == max_draft_limit:
                    datalist.append('Final Document is ready')
                elif op.oi_status == 181:
                    datalist.append('Waiting For Input')
                else:
                        datalist.append(op.get_user_oi_status)
                if oi.oi_status == 2 and op.oi_status == 2:
                    options.append('Upload Resume')
                elif op.oi_status == 24 or op.oi_status == 27:
                    options.append({'Download':"dashboard:dashboard-resumedownload"+oi.order.pk+':+?path='+op.oi_draft.name})

        elif oi.product.type_flow == 8:
            for op in ops:
                date_created =op.created
                if op.oi_status == 46 and op.draft_counter == 1:
                    datalist.append(op.get_user_oi_status)
                elif op.oi_status == 46 and op.draft_counter < max_draft_limit:
                    datalist.append('Revised Document is ready')
                elif op.oi_status == 4:
                    datalist.append('Document is finalized')
                elif op.oi_status == 181:
                    datalist.append('Waiting for input')
                else:
                    datalist.append(op.get_user_oi_status)
                if op.oi_status == 2 and oi.oi_status == 2:
                    options.append('Upload Resume')
                elif op.oi_status == 46 or op.oi_status == 27:
                    options.append({'Download':"linkedin-draf-download"+oi.pk+" "+ op.pk})

        elif oi.product.type_flow == 3:
            for op in ops:
                date_created =op.created
                datalist.append(op.get_user_oi_status)
                if op.oi_draft:
                    options.append({'Download':"dashboard:dashboard-resumedownload"+oi.order.pk+':+?='+op.oi_draft.name})
                elif oi.oi_status == 2 and op.oi_status == 2:
                    options.append('Upload Resume')
        elif oi.product.type_flow == 2 or  oi.product.type_flow == 14:
            for op in ops:
                date_created =op.created
                datalist.append(op.get_user_oi_status)
                if op.oi_status == 6:
                    options.append({'Download':"dashboard:dashboard-resumedownload"+oi.order.pk+':?='+op.oi_draft.name})
        elif oi.product.type_flow == 4:
            for op in ops:
                date_created =op.created
                datalist.append(op.get_user_oi_status)
                if oi.oi_status == 2 and not oi.oi_resume:
                    options.append('Upload Resume')
                elif op.oi_status == 6:
                    options.append({'Download Credential':"url 'console:profile_credentials' oi.pk"})
        elif oi.product.type_flow == 5:
            if oi.product.sub_type_flow == 502:
                with oi.get_item_operations as custom_ops:
                    for op in custom_ops:
                        date_created =op.created
                        if op.oi_status == 31:
                            datalist.append('Service is Under Progress')
                        else:
                            datalist.append(op.get_user_oi_status)
            else:
                for op in ops:
                    date_created =op.created
                    datalist.append(op.get_user_oi_status)
                    if oi.oi_status == 2 and not oi.oi_resume and op.oi_status == 2:
                        options.append('Upload Resume')

        elif oi.product.type_flow == 6:
            for op in ops:
                date_created =op.created
                datalist.append(op.get_user_oi_status)
                if op.oi_draft:
                    options.append({'Download':"dashboard:dashboard-resumedownload"+oi.order.pk+':?path='+op.oi_draft.name})
        elif oi.product.type_flow == 7 or oi.product.type_flow == 15:
            for op in ops:
                date_created =op.created
                datalist.append(op.get_user_oi_status)
                if oi.oi_status == 2 and not oi.oi_resume and op.oi_status == 2:
                    options.append('Upload Resume')
        elif oi.product.type_flow == 9:
            for op in ops:
                date_created =op.created
                datalist.append(op.get_user_oi_status)
                if op.oi_status == 141:
                    options.append('Complete Profile')
                elif op.oi_status == 142:
                    options.append('Edit your profile')
        elif oi.product.type_flow == 10:
            for op in ops:
                date_created =op.created
                datalist.append(op.get_user_oi_status)
                if op.oi_status == 101:
                    options.append('Take Test')
                elif op.oi_draft:
                    options.append({'Download':"dashboard:dashboard-resumedownload"+oi.order.pk+':?path='+op.oi_draft.name})
        elif oi.product.type_flow == 17:
            for op in ops:
                date_created =op.created
                datalist.append(op.get_user_oi_status)
                if op.oi_status == 101:
                    options.append('Take Test')
                elif op.oi_draft:
                    options.append({'Download':"dashboard:dashboard-resumedownload"+oi.order.pk+':?path='+op.oi_draft.name})
        return {
                'date_created':date_created,
                'datalist':datalist,
                'options':options
                }

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
                'status':self.get_oi_status_value(instance) if instance.oi_status else None,
                'mode':instance.product.get_studymode_db(),
                'jobs':instance.product.num_jobs,
            })
            # course_detail = self.get_courses_detail(instance)
            # data.update({
            #     'date_created':course_detail['date_created'],
            #     'datalist':course_detail['datalist'],
            #     'options':course_detail['options']
            #     })
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
