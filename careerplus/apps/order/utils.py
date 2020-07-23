# python imports
from decimal import Decimal
import calendar
from datetime import date, datetime,timedelta
import logging
from dateutil import relativedelta
import json,copy

# django imports
from django.db.models import Sum
from django.core.cache import cache
from django.utils import timezone

#inter app import
from emailers.tasks import send_email_task
from emailers.sms import SendSMS
from emailers.utils import BadgingMixin
from users.tasks import user_register
from shop.choices import S_ATTR_DICT, A_ATTR_DICT




def get_ltv(candidate_id, till_month=None):

    from order.models import Order, OrderItem, RefundRequest
    ltv = Decimal(0)
    if till_month:
        month = till_month
        year = datetime.now().year
        date_one_year_ago = datetime(year=year, month=month, day=1) - relativedelta.relativedelta(year=1) # calculate last year start of month
        date_one_year_after = datetime(year=year, month=month, day=1) + relativedelta.relativedelta(months=1) # calcualing till last of month
        filter_kwargs = {
            'candidate_id': candidate_id,
            'status__in': [1, 2, 3],
            'payment_date__gte': date_one_year_ago,
            'payment_date__lte': date_one_year_after
        }
    else:
        date_one_year_ago = datetime.now() - timedelta(days=365)
        filter_kwargs = {
            'candidate_id': candidate_id,
            'status__in': [1, 2, 3],
            'payment_date__gte': date_one_year_ago,
        }

    # Consider only last 1 year's orders for LTV.

    ltv_pks = list(Order.objects.filter(**filter_kwargs).values_list('pk', flat=True))

    if ltv_pks:
        ltv_order_sum = Order.objects.filter(
            pk__in=ltv_pks).aggregate(ltv_price=Sum('total_incl_tax'))
        last_order = OrderItem.objects.select_related('order').filter(order__in = ltv_pks)\
            .exclude(oi_status=163).order_by('-order__payment_date').first()
        if last_order:
            last_order = last_order.order.payment_date.strftime('%Y-%m-%d %H:%M:%S')
        else:
            last_order = ""

        ltv = ltv_order_sum.get('ltv_price') if ltv_order_sum.get('ltv_price') else Decimal(0)
        rf_ois = list(OrderItem.objects.filter(
            order__in=ltv_pks,
            oi_status=163).values_list('order', flat=True))

        rf_sum = RefundRequest.objects.filter(
            order__in=rf_ois).aggregate(rf_price=Sum('refund_amount'))
        if rf_sum.get('rf_price'):
            ltv = ltv - rf_sum.get('rf_price')

    return ltv

class LTVReportUtil:
    '''
        Util to generate LTV report with following functions
        1. get ltv bracket of candidate with candidate id
    '''
    LTV_BRACKETS = [(0,5000),
                                (5001,10000),
                                (10001,20000),
                                (20001,40000),
                                (40001,60000),
                                (60001,80000),
                                (80001,100000),
                                (100001,125000),
                                (125001,150000),
                                (150001,175000),
                                (175001,10000000)
                            ]
                                    
    LTV_BRACKET_LABELS = ["0-5k","5-10k","10-20k","20-40k","40-60k","60-80k",\
            "80-100k","100-125k","125-150k","150-175k","175k+"]

    def get_ltv_bracket(self, candidate_id, till_month=None):
        ltv = get_ltv(candidate_id, till_month) if candidate_id else 0
        ltv_bracket = ''
        for pos, bracket in enumerate(self.LTV_BRACKETS):
            if bracket[0] <= int(ltv) and bracket[1] >= int(ltv):
                ltv_bracket = self.LTV_BRACKET_LABELS[pos]
                break
        return ltv_bracket

    # def generate_report(self,year,month):


    def get_monthly_ltv_record(self,year,month):
        from order.models import MonthlyLTVRecord

        return MonthlyLTVRecord.objects.filter(
            year=year, month=month
        )

    def create_monthly_ltv_record(self, year, month):
        from order.models import MonthlyLTVRecord, Order
        year = int(year)
        month = int(month)

        logging.getLogger('info_log').info('Monthly ltv cron started for year - {} month - {}'.format(year, month))
        start_date = date(year, month, 1)
        end_date = start_date + relativedelta.relativedelta(months=1)

        orders = Order.objects.filter(
            payment_date__gte=start_date,
            payment_date__lte=end_date,\
            status__in=[1, 3])

        candidate_id_order_mapping = {}

        for order in orders:
            if not order.candidate_id:
                continue

            previous_data = candidate_id_order_mapping.get(order.candidate_id,[])
            previous_data.append(order)
            candidate_id_order_mapping.update({order.candidate_id:previous_data})

        candidate_id_ltv_mapping = {}
        ltv_bracket_record_mapping = {}
        logging.getLogger('info_log').info('No of unique candidate ids are- {} '.format(len(candidate_id_order_mapping.keys())))

        for candidate_id in candidate_id_order_mapping.keys():
            ltv_bracket = self.get_ltv_bracket(candidate_id, till_month=month)
            logging.getLogger('info_log').info('candidate id - {} in ltv bracket - {}'.format(candidate_id,ltv_bracket))

            if ltv_bracket in candidate_id_ltv_mapping:
                candidate_id_ltv_mapping[ltv_bracket].append(candidate_id)
            else:
                candidate_id_ltv_mapping[ltv_bracket] = [candidate_id]

            previous_data = ltv_bracket_record_mapping.get(ltv_bracket)
            total_users = 1
            crm_order_ids,learning_order_ids = [],[]
            crm_item_count,learning_item_count = 0 , 0

            for order in candidate_id_order_mapping.get(candidate_id,[]):
                oi_actual_price_mapping = order.get_oi_actual_price_mapping()
                count = len(oi_actual_price_mapping.keys())
                if order.sales_user_info:
                    crm_item_count += count
                    crm_order_ids.append(order.id)
                else:
                    learning_item_count += count
                    learning_order_ids.append(order.id)

            if previous_data:
                crm_order_ids += (previous_data.get('crm_order_ids', []))
                learning_order_ids += (previous_data.get('learning_order_ids', []))
                learning_item_count += previous_data.get('learning_item_count', 0)
                crm_item_count += previous_data.get('crm_item_count', 0)

            ltv_bracket_record_mapping.update({
                ltv_bracket: {
                    'crm_order_ids': crm_order_ids,
                    'learning_order_ids': learning_order_ids,
                    'learning_item_count': learning_item_count,
                    'crm_item_count': crm_item_count,
                }
            })

        logging.getLogger('info_log').info('Received records for different ltv brackets')
        default_record = {
            'crm_order_ids': [],
            'learning_order_ids': [],
            'learning_item_count': 0,
            'crm_item_count': 0,
        }

        for index, bracket in enumerate(self.LTV_BRACKET_LABELS):
            new_record = ltv_bracket_record_mapping.get(bracket,'')

            if not new_record:
                new_record = copy.deepcopy(default_record)
                logging.getLogger('info_log').info('No candidate in ltv bracket - {}'.format(bracket))

            candidate_ids = candidate_id_ltv_mapping.get(bracket, [])
            crm_order_ids = json.dumps(new_record.get('crm_order_ids'))
            learning_order_ids =  json.dumps(new_record.get('learning_order_ids'))
            new_record.update({
                'crm_order_ids': crm_order_ids,
                'learning_order_ids': learning_order_ids,
                'ltv_bracket': index,
                'candidate_ids': json.dumps(candidate_ids)
            })

            obj, created = MonthlyLTVRecord.objects.update_or_create(
                year=year, month=month, ltv_bracket=index,
                defaults=new_record,
            )

            if created:
                logging.getLogger('info_log').info('Created a record for ltv bracket - {}'.format(bracket))
            else:
                logging.getLogger('info_log').info('Updated a record for ltv bracket - {}'.format(bracket))

class FeatureProfileUtil:

    def get_featured_oi(self,oi_status,sub_type_flow):
        from  order.models import OrderItem
        return OrderItem.objects.filter(
                order__status__in=[1, 3], product__type_flow__in=[5], oi_status__in=oi_status,
                product__sub_type_flow__in=sub_type_flow).select_related('order')

    def get_candidate_id(self,oi):
        from order.models import Order
        candidate_id = oi.order.candidate_id 

        if not candidate_id:
            user_register(data={}, order=oi.order.pk)
            order = Order.objects.get(pk=oi.order.pk)
            candidate_id = oi.order.candidate_id
        
        return candidate_id

    def update_badges(self,candidate_id,oi,feature):
        badge_data = BadgingMixin().get_badging_data(
                        candidate_id=candidate_id, curr_order_item=oi, feature=feature
                    )        
        flag = BadgingMixin().update_badging_data(candidate_id=candidate_id, data=badge_data)
        if flag:
            logging.getLogger('info_log').info(
                        'Feature:- Data sent to shine for order item %s is %s' % (str(oi.id), str(badge_data))
                    )
        return flag
    
    def create_oi_operation(self,oi,oi_status,last_oi_status):
        oi.orderitemoperation_set.create(
                oi_status=oi_status,
                last_oi_status=last_oi_status,
                assigned_to=oi.assigned_to)
        return


    def pause_resume_feature(self,oi,isPause=True):
        from  order.models import OrderItem
        candidate_id = self.get_candidate_id(oi)
        pause_resume_operations = oi.orderitemoperation_set.filter(oi_status__in=[34,35])

        if pause_resume_operations:
            last_op_date = pause_resume_operations.last().created
            time_diff = timezone.now() - last_op_date
            if time_diff.days == 0:    
                return False

        if isPause:
            other_item_exist = OrderItem.objects.filter(
                    order__status__in=[1, 3], product__type_flow__in=[5],
                    oi_status=28,
                    product__sub_type_flow=oi.product.sub_type_flow,
                    order__candidate_id=oi.order.candidate_id).exclude(id=oi.id).exists()

            if other_item_exist:
                return True
                
        flag = self.update_badges(candidate_id,oi,isPause)

        if not flag:
            logging.getLogger('info_log').info(
                'Badging Failed {} '.format(str(oi.id))
            )
            return False
        return True
    def start_all_feature(self):
        oi_status =[30,38]
        sub_type_flow = [501,503,504]
        featured_orderitems = self.get_featured_oi(oi_status,sub_type_flow)
        featured_count = 0
        applicant_count = 0
        for oi in featured_orderitems:
            candidate_id = self.get_candidate_id(oi)
            flag = self.update_badges(candidate_id,oi,True)
            if not flag:
                logging.getLogger('info_log').info(
                    'Badging Failed {} '.format(str(oi.id))
                )
                continue
            if oi.product.sub_type_flow == 504 :
                applicant_count +=1
                oi.oi_status = 36
                
            else :
                featured_count += 1
                oi.oi_status = 28
                

            last_oi_status = oi.oi_status
            oi.closed_on = timezone.now()
            oi.last_oi_status = 6
            oi.start_date = timezone.now()
            oi.end_date = timezone.now() + timedelta(days=oi.product.day_duration)
            oi.save()
            self.create_oi_operation(oi,6,last_oi_status)
            self.create_oi_operation(oi,oi.oi_status,oi.last_oi_status)

            # Send mail and sms with subject line as Your Profile updated
            self.send_feature_mail(oi)
            
       
        if applicant_count : 
            out_str = '%s top applicant profile featured out of %s' % (
                applicant_count, featured_orderitems.count())
            logging.getLogger('info_log').info("{}".format(out_str))
        
        if featured_count : 
            out_str = '%s profile featured out of %s' % (
                featured_count, featured_orderitems.count())
            logging.getLogger('info_log').info("{}".format(out_str))

        return

    

    def close_all_feature(self):
        from order.models import OrderItem
        oi_status = [28,34,35,36]
        sub_type_flow = [501,503,504]
        featured_orderitems = self.get_featured_oi(oi_status,sub_type_flow)
        unfeature_count = 0

        for oi in featured_orderitems:
            candidate_id = self.get_candidate_id(oi)
            days_left = oi.days_left_oi_product

            if not candidate_id or  days_left >= 0:
                logging.getLogger('info_log').info(
                    'Days remaining {} '.format(days_left)
                )
                continue

            other_item_exist = OrderItem.objects.filter(
                    order__status__in=[1, 3], product__type_flow__in=[5],
                    oi_status__in=[28,36],
                    product__sub_type_flow=oi.product.sub_type_flow,
                    order__candidate_id=oi.order.candidate_id).exclude(id=oi.id).exists()

            
            if not other_item_exist:
                flag = self.update_badges(candidate_id,oi,False)
                if not flag:
                    logging.getLogger('info_log').info(
                        'Badging Failed for order item id %s' % (str(oi.id)))
                    continue
            last_oi_status = oi.oi_status

            if oi.product.sub_type_flow == 504 :
                oi.last_oi_status = 37
                self.create_oi_operation(oi,37,last_oi_status)
            else:
                oi.last_oi_status = 29
                self.create_oi_operation(oi,29,last_oi_status)
            unfeature_count += 1
            
            oi.oi_status = 4
            oi.closed_on = timezone.now()
            
            oi.save()
            
            self.create_oi_operation(oi,oi.oi_status,oi.last_oi_status)

        out_str = '%s profile expired out of %s featured items' % (
            unfeature_count, featured_orderitems.count())

        logging.getLogger('info_log').info("{}".format(out_str))
        return

   

    def send_feature_mail(self,oi):
        if oi.product.sub_type_flow == 501:
            mail_type = "FEATURED_PROFILE_UPDATED"
        elif oi.product.sub_type_flow == 503:
            mail_type = "PRIORITY_APPLICANT_MAIL"
        elif oi.product.sub_type_flow == 504:
            mail_type = "TOP_APPLICANT_MAIL"

        email_sets = list(
            oi.emailorderitemoperation_set.all().values_list(
                'email_oi_status', flat=True).distinct())
        to_emails = [oi.order.get_email()]
        data = {}
        if oi.product.sub_type_flow == 504:
            data.update({
            "subject": 'Your Top Applicant Service is Initiated',
            "username": oi.order.first_name,
            "product_timeline": oi.product.get_duration_in_day(),
            })
        else :
            data.update({
            "subject": 'Your Featured Profile Is Updated',
            "username": oi.order.first_name,
            "product_timeline": oi.product.get_duration_in_day(),
            })
        

        if 72 not in email_sets:
            send_email_task.delay(
                to_emails, mail_type, data,
                status=72, oi=oi.pk)

        SendSMS().send(sms_type=mail_type, data=data)
                    





