#python imports
import logging
from decimal import Decimal
from datetime import datetime, timedelta
from dateutil import relativedelta
import ast,os,django,sys,csv,json,pytz

#Settings imports
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careerplus.config.settings_live")
ROOT_FOLDER = os.path.realpath(os.path.dirname(__file__))
ROOT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')]
if ROOT_FOLDER not in sys.path:
    sys.path.insert(1, ROOT_FOLDER + '/')
django.setup()

#django imports
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.exceptions import ImproperlyConfigured
from django.core.cache import cache

#local imports

#inter app imports
from coupon.models import Coupon
from payment.models import PaymentTxn
from shop.choices import DURATION_DICT,EXP_DICT
from order.models import Order,OrderItem,CouponOrder, RefundItem
from core.library.gcloud.custom_cloud_storage import GCPPrivateMediaStorage
from users.mixins import WriterInvoiceMixin
from order.utils import get_ltv, LTVReportUtil

#third party imports

class ShineCandidate:
    """
    To save Shine candidate Detail data.
    Save this in redis to extract user from token.

    Sample Data - 

    {'bad_words_fields': {},
     'certifications': [],
     'id':'53ff1c11350d9d1f41ababfd',
     'candidate_id':'53ff1c11350d9d1f41ababfd',
     'desired_job': [{'candidate_id': '53ff1c11350d9d1f41ababfd',
       'candidate_location': [242],
       'functional_area': [1301],
       'industry': [0],
       'job_type': [0],
       'maximum_salary': [13],
       'minimum_salary': [7],
       'shift_type': [1]}],
     'education': [{'candidate_id': '53ff1c11350d9d1f41ababfd',
       'course_type': 1,
       'education_level': 110,
       'education_specialization': 503,
       'id': '5b3a69b94998e2428d0adfa6',
       'institute_name': 'Delhi College of Engineering',
       'year_of_passout': 2014}],
     'is_bad_word_present': False,
     'jobs': [{'candidate_id': '53ff1c11350d9d1f41ababfd',
       'company_name': 'HT Media',
       'description': '',
       'end_date': None,
       'end_month': None,
       'end_year': None,
       'id': '55655a68d6a4923b516efd42',
       'industry_id': 18,
       'industry_id_display_value': 'IT - Software',
       'is_current': True,
       'job_title': 'Python Developer',
       'job_title_lookup_id': None,
       'start_date': '2014-07-01T00:00:00',
       'start_month': 7,
       'start_year': 2014,
       'sub_field': 4530,
       'sub_field_display_value': 'Web / Mobile Technologies'}],
     'personal_detail': [{'candidate_location': 423,
       'cell_phone': '9717114180',
       'country_code': '91',
       'date_of_birth': '1991-12-20',
       'email': 'sanimesh007@gmail.com',
       'first_name': 'Animesh',
       'gender': 1,
       'id': '53ff1c11350d9d1f41ababfd',
       'is_cell_phone_verified': 0,
       'is_email_verified': 1,
       'is_featured_by_career_plus': False,
       'last_name': 'Sharma',
       'profile_badges': [],
       'resume_title': 'Software Engineer'}],
     'resumes': [{'candidate_id': '53ff1c11350d9d1f41ababfd',
       'creation_date': '2018-07-02T23:37:19',
       'extension': 'pdf',
       'id': '5b3a69d707fe270bf686c670',
       'is_default': 1,
       'resume_name': 'Animesh Sharma - Resume_02-Jul-18_23:37:20'}],
     'skills': [{'candidate_id': '53ff1c11350d9d1f41ababfd',
       'id': '5b3a6a724998e244038b7083',
       'value': 'Python',
       'years_of_experience': 7,
       'years_of_experience_display_value': '4 Yrs'},
      {'candidate_id': '53ff1c11350d9d1f41ababfd',
       'id': '5b3a6a7a9924592cf8c39222',
       'value': 'Django',
       'years_of_experience': 7,
       'years_of_experience_display_value': '4 Yrs'},
      {'candidate_id': '53ff1c11350d9d1f41ababfd',
       'id': '5b3a6a8807fe270b4263bc8a',
       'value': 'Rest APIs / Framework',
       'years_of_experience': 7,
       'years_of_experience_display_value': '4 Yrs'},
      {'candidate_id': '53ff1c11350d9d1f41ababfd',
       'id': '5b3a6a944998e2434e67e0f1',
       'value': 'Solr / Lucene',
       'years_of_experience': 7,
       'years_of_experience_display_value': '4 Yrs'},
      {'candidate_id': '53ff1c11350d9d1f41ababfd',
       'id': '5b3a6a9d445b890b2befbca3',
       'value': 'MongoDB',
       'years_of_experience': 7,
       'years_of_experience_display_value': '4 Yrs'},
      {'candidate_id': '53ff1c11350d9d1f41ababfd',
       'id': '5b3a6aa89924592ef89311cf',
       'value': 'MySQL',
       'years_of_experience': 7,
       'years_of_experience_display_value': '4 Yrs'}],
     'total_experience': [{'experience_in_months': 0, 'experience_in_years': 7}],
     'workex': [{'experience_in_months': 0,
       'experience_in_years': 7,
       'id': '53ff1c11350d9d1f41ababfd',
       'notice_period': 0,
       'notice_period_last_working_date': None,
       'previous_salary': 7,
       'resume_title': 'Software Engineer',
       'salary_in_lakh': 3,
       'salary_in_thousand': 0,
       'summary': 'Experienced Web Developer with a demonstrated history of working in the internet industry. Skilled in Python, SQL, Solr, MongoDB, and Data Structures. Strong engineering professional with a B.Tech focused in Computer Science from Delhi College of Engineering.',
       'team_size_managed': 3}]}
    """

    def is_authenticated(self):
        return True

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return self.candidate_id


class DiscountReportUtil:

    def __init__(self,**kwargs):
        self.start_date = pytz.utc.localize(kwargs.get('start_date'))
        self.end_date = pytz.utc.localize(kwargs.get('end_date'))
        self.file_name = kwargs.get('file_name')
        self.filter_type = kwargs.get('filter_type',1)

        if not self.start_date or not self.end_date or not self.file_name:
            raise ImproperlyConfigured("Please provide start_date and end_date")

        if self.start_date > self.end_date:
            raise ImproperlyConfigured("start_date must be less than end_date")

    def get_file_obj(self,file_name):
        if settings.IS_GCP:
            generated_file_obj = GCPPrivateMediaStorage().open(file_name, 'wb')
        else:
            generated_file_obj = open(settings.MEDIA_ROOT + '/' + file_name, 'w')
        return generated_file_obj

    def generate_report(self):
        file_obj = self.get_file_obj(self.file_name)
        csv_writer = csv.writer(file_obj, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(["order_id","Candidate Id","Owner_name","Order_Date","Payment_Date","Payment Time",\
                    "Last Payment Date","Last Payment Time","Sales_executive","Sales_TL",\
                    "Branch_Head","Transaction_ID","item_id","Product Id","Product_Name","Functional Area",\
                    "Item_Name","Experience","Course Duration","Status",\
                    "Price of item on site according to order (without tax including context)",\
                    "Discount (includes wallet and coupon)","Price of order with no discount/wallet",\
                    "Actual collection of order","Effective collection per item",\
                    "Delivery Service","Delivery Price Incl Tax","Delivery Price Excl Tax",\
                    "Price of item on site","Transaction_Amount","coupon_id",\
                    "Payment_mode","Combo", "Combo Parent","Variation","Refunded","Refund Amount",\
                    "No Process", "Replaced", "Replaced With", "Replacement Of","Writer price excluding Incentives",\
                    "Writer's name", "Lead Type",'LTV Bracket'])

        if int(self.filter_type) == 1:  # get order item based on payment_date filter
            transactions = PaymentTxn.objects.filter(status=1,\
                payment_date__gte=self.start_date,payment_date__lte=self.end_date)
            order_ids = list(transactions.values_list('order_id',flat=True))
            orders = Order.objects.filter(status__in=[1,3],id__in=order_ids).order_by('id')
        
        elif int(self.filter_type) == 2: # get order item based on order created date filter
            orders = Order.objects.filter(\
              status__in=[1,3],payment_date__gte=self.start_date,payment_date__lte=self.end_date)

        logging.getLogger('info_log').info("\
            Discount Report :: Total orders found - {}".format(orders.count()))

        for order in orders:
            order_items = OrderItem.objects.filter(order=order)
            try:
                sales_user_info = json.loads(order.sales_user_info)
            except Exception as e:
                try:
                    sales_user_info = ast.literal_eval(order.sales_user_info)
                except Exception as e:
                    logging.getLogger('error_log').error("\
                            Error - {}".format(e))
                    sales_user_info = {}
                
            txn_obj_list = order.get_txns().filter(status=1)
            txn_obj = txn_obj_list.first()
            last_txn_obj = txn_obj_list.order_by('-id').first()
            transaction_ids = ", ".join([x.txn for x in txn_obj_list])
            coupon_order = CouponOrder.objects.filter(order=order).first()
            coupon_code = coupon_order.coupon_code if coupon_order else ""
            replaced = False
            replacement_id = None
            order_discount = sum(order_items.values_list('discount_amount',flat=True))
            order_cost_price = sum(order_items.values_list('cost_price',flat=True))
            order_selling_price = sum(order_items.values_list('selling_price',flat=True))
            price_without_wallet_discount = round(float(order.total_incl_tax) + \
                float(order_discount) * float(1.18),2)

            coupon_objs = Coupon.objects.filter(\
                        id__in=order.couponorder_set.values_list('coupon',flat=True))

            forced_coupon_amount = 0
            for obj in coupon_objs:
                amount = float(obj.value) if obj.coupon_type == "flat" else \
                    float((obj.value*order.total_excl_tax) / 100)
                forced_coupon_amount += amount

            for item in order_items:
                if not item.product:
                    logging.getLogger('error_log').error("Item {} has no product attached".format(item.id))
                    continue

                combo_parent = False
                item_delivery_service = item.delivery_service.display_name if item.delivery_service else ""
                item_selling_price = item.selling_price
                item_cost_price = float(item.cost_price)
                item_discount_price = float(item.discount_amount)
                if not item_cost_price:
                    item_cost_price = float(item.product.inr_price)
                # check the discount_price with cost_price for free_product
                if item.product.type_product == 0 and item_selling_price == 0 \
                    and not item.is_combo and not item.no_process \
                        and item_discount_price != item_cost_price:
                    item_selling_price = float((float(item.product.inr_price) - forced_coupon_amount)) * 1.18

                item_refund_request_list = RefundItem.objects.filter(oi_id=item.id,\
                        refund_request__status__in=[1,3,5,7,8,11])
                refund_amount = item_refund_request_list.first().amount \
                    if item_refund_request_list else 0

                if item.is_combo and item.parent:
                    parent_sum = float(item.parent.cost_price)
                    if not parent_sum:
                        #Assuming price remains unchanged
                        parent_sum = float(item.parent.product.inr_price)
                        order_discount = float(forced_coupon_amount)

                    actual_sum_of_child_combos = 0
                    child_combos = item.order.orderitems.filter(parent=item.parent)

                    for child_combo in child_combos:
                        child_cost_price = float(child_combo.cost_price)
                        if not child_cost_price:
                            child_cost_price = float(child_combo.product.inr_price)
                        actual_sum_of_child_combos += child_cost_price

                    virtual_decrease_in_price = actual_sum_of_child_combos - parent_sum
                    virtual_decrease_part_of_this_item = virtual_decrease_in_price * \
                        (float(item_cost_price) / actual_sum_of_child_combos)
                    actual_price_of_item_after_virtual_decrease = float(item_cost_price) - \
                        virtual_decrease_part_of_this_item

                    if order_discount > 0:
                        combo_discount_amount = (float(order_discount) / \
                            float(order.total_excl_tax)) * \
                                actual_price_of_item_after_virtual_decrease
                        actual_price_of_item_after_virtual_decrease -= combo_discount_amount

                    item_selling_price = round((actual_price_of_item_after_virtual_decrease * 1.18), 2)
                    item_refund_request_list = RefundItem.objects.filter(oi_id=item.parent.id,\
                        refund_request__status__in=[1,3,5,7,8,11])
                    total_refund = float(item_refund_request_list.first().amount) \
                        if item_refund_request_list else 0

                    if item.parent.selling_price:
                        refund_amount = round(total_refund * (item_selling_price / \
                            float(item.parent.selling_price)),2)
                    else:
                        refund_amount = 0

                if item.is_combo and not item.parent:
                    combo_parent = True
                    item_selling_price = 0
                    refund_amount = 0

                if item.wc_sub_cat == 65:
                    replaced = True
                    replacement_id = item.get_replacement_order_id

                total_items = item.order.orderitems.count()
                if total_items == 1 and item_selling_price == 0 and item_discount_price != item_cost_price:
                    item_selling_price = float(float(order.total_excl_tax) - forced_coupon_amount)*1.18

                writer_price = 0
                writer_name = ''
                if item.order.status in [1,3] and item.product.type_flow in [1, 8, 12, 13] and \
                        item.oi_status == 4 and item.assigned_to and item.closed_on >= self.start_date\
                            and item.closed_on <= self.end_date:
                    invoice_date = item.closed_on.replace(day=1).date()  
                    invoice_date = invoice_date - timedelta(days=1)
                    invoice_date =invoice_date + relativedelta.relativedelta(months=1)
                    writer_invoice = WriterInvoiceMixin(invoice_date)
                    user_profile = writer_invoice.check_user_profile(item.assigned_to)
                    if not user_profile['error']:
                        writer_invoice.set_user_type(item.assigned_to)
                        total_sum,total_combo_discount,success_closure = writer_invoice.get_writer_details_per_oi(item,item.assigned_to) 
                        writer_price = total_sum - total_combo_discount
                        writer_name = item.assigned_to if item.assigned_to else ''

                logging.getLogger('error_log').error(\
                        "sales_user_info_Data  {} | {}".format(sales_user_info.get('is_upsell'),sales_user_info.get('executive')))

                lead_type = 'NA'
                if 'is_upsell' in sales_user_info:
                    lead_type = 'Upsell' if sales_user_info.get('is_upsell') else 'Fresh'

                ltv_bracket = LTVReportUtil().get_ltv_bracket(candidate_id=order.candidate_id)
                product = item.product
                main_category = product.category_main
                lv2_parent = 'NA'   #default
                if main_category:
                    lv2_parent  = main_category.get_parent().first()
                    lv2_parent = lv2_parent.name if lv2_parent else 'NA'

                try:
                    row_data = [
                        order.id,order.candidate_id,item.partner.name,order.date_placed.date(),\
                        txn_obj.payment_date.date(),txn_obj.payment_date.time(),\
                        last_txn_obj.payment_date.date(),last_txn_obj.payment_date.time(),\
                        sales_user_info.get('executive',''),\
                        sales_user_info.get('team_lead',''),sales_user_info.get('branch_head',''),\
                        transaction_ids,item.id,item.product.id,item.product.name,lv2_parent,item.product.heading,\
                        EXP_DICT.get(item.product.get_exp(),"N/A"), \
                        DURATION_DICT.get(item.product.get_duration(),"N/A"),order.get_status,\
                        item_cost_price,order_discount,price_without_wallet_discount,order.total_incl_tax,\
                        float(item_selling_price)+float(item.delivery_price_incl_tax),\
                        item_delivery_service,float(item.delivery_price_incl_tax),\
                        float(item.delivery_price_excl_tax),item_cost_price,order.total_incl_tax,\
                        coupon_code,txn_obj.get_payment_mode(),item.is_combo, combo_parent,item.is_variation,\
                        bool(item_refund_request_list),refund_amount,item.no_process, replaced, replacement_id,\
                        order.replaced_order,writer_price,writer_name,lead_type,ltv_bracket
                    ]

                    csv_writer.writerow(row_data)

                except Exception as e:
                    logging.getLogger('error_log').error(\
                        "Discount Report | Order {} | {}".format(order.id,repr(e)))
                    continue
        file_obj.close()



# over come the datetime objects to json

def default(obj):
    if type(obj) is datetime.date or type(obj) is datetime:
        return obj.strftime("%d %b, %Y")

def jsondumps(obj):
    return json.dumps(obj, default=default)




    

    








