# python imports
from decimal import Decimal
import calendar
from datetime import date, datetime,timedelta
import logging
from dateutil import relativedelta
import json

# django imports
from django.db.models import Sum
from django.core.cache import cache

#in app import


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
        from order.models import LTVMonthlyRecord

        return LTVMonthlyRecord.objects.filter(
            year=year, month=month
        )

    def create_monthly_ltv_record(self, year, month):
        from order.models import LTVMonthlyRecord, Order
        year = int(year)
        month = int(month)

        logging.getLogger('info_log').info('Monthly ltv cron started for year - {} month - {}'.format(year, month))
        start_date = date(year, month, 1)
        end_date = start_date + relativedelta.relativedelta(months=1)

        orders = Order.objects.filter(
            payment_date__gte=start_date,
            payment_date__lte=end_date,\
            status__in=[1, 3])

        unique_candidate_ids = list(set([x.candidate_id for x in orders]))
        candidate_id_ltv_mapping = {}
        ltv_bracket_record_mapping = {}
        logging.getLogger('info_log').info('No of unique candidate ids are- {} '.format(len(unique_candidate_ids)))

        for candidate_id in unique_candidate_ids:
            ltv_bracket = self.get_ltv_bracket(candidate_id, till_month=month)
            logging.getLogger('info_log').info('candidate id - {} in ltv bracket - {}'.format(candidate_id,ltv_bracket))

            if ltv_bracket in candidate_id_ltv_mapping:
                candidate_id_ltv_mapping[ltv_bracket].append(candidate_id)
            else:
                candidate_id_ltv_mapping[ltv_bracket] = [candidate_id]
            previous_data = ltv_bracket_record_mapping.get(ltv_bracket)
            total_users = 1
            total_orders = Order.objects.filter(
                candidate_id=candidate_id, payment_date__gte=start_date,\
                payment_date__lte=end_date, status__in=[1, 3])
            total_order_count = total_orders.count()
            total_item_count = 0
            crm_order_count, crm_item_count = 0, 0
            learning_order_count, learning_item_count = 0, 0

            for order in total_orders:
                oi_actual_price_mapping = order.get_oi_actual_price_mapping()
                count = len(oi_actual_price_mapping.keys())
                total_item_count += count
                if order.sales_user_info:
                    crm_item_count += count
                    crm_order_count += 1
                else:
                    learning_item_count += count
                    learning_order_count += 1

            if previous_data:
                total_users += previous_data.get('total_users', 0)
                total_item_count += previous_data.get('total_item_count', 0)
                total_order_count += previous_data.get('total_order_count', 0)
                crm_item_count += previous_data.get('crm_item_count', 0)
                crm_order_count += previous_data.get('crm_order_count', 0)
                learning_item_count += previous_data.get('learning_item_count', 0)
                learning_order_count += previous_data.get('learning_order_count', 0)

            ltv_bracket_record_mapping.update({
                ltv_bracket: {
                    'total_users': total_users,
                    'total_item_count': total_item_count,
                    'total_order_count': total_order_count,
                    'crm_item_count': crm_item_count,
                    'crm_order_count': crm_order_count,
                    'learning_item_count': learning_item_count,
                    'learning_order_count': learning_order_count
                }
            })

        logging.getLogger('info_log').info('Received records for different ltv brackets')

        default_record = {
            'total_users': 0,
            'total_item_count': 0,
            'total_order_count': 0,
            'crm_item_count': 0,
            'crm_order_count': 0,
            'learning_item_count': 0,
            'learning_order_count': 0
        }

        for index, bracket in enumerate(self.LTV_BRACKET_LABELS):
            new_record = ltv_bracket_record_mapping.get(bracket,'')

            if not new_record:
                new_record = default_record
                logging.getLogger('info_log').info('No candidate in ltv bracket - {}'.format(bracket))

            candidate_ids = candidate_id_ltv_mapping.get(bracket, [])
            new_record.update({
                'ltv_bracket': index,
                'candidate_id_ltv_mapping': json.dumps(candidate_ids)
            })

            obj, created = LTVMonthlyRecord.objects.update_or_create(
                year=year, month=month, ltv_bracket=index,
                defaults=new_record,
            )

            if created:
                logging.getLogger('info_log').info('Created a record for ltv bracket - {}'.format(bracket))
            else:
                logging.getLogger('info_log').info('Updated a record for ltv bracket - {}'.format(bracket))





