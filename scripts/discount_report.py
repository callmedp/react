#python imports
import logging
from decimal import Decimal
from datetime import datetime, timedelta
import ast,os,django,sys,subprocess,csv

#Settings imports
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careerplus.config.settings")
ROOT_FOLDER = os.path.realpath(os.path.dirname(__file__))
ROOT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')]
if ROOT_FOLDER not in sys.path:
    sys.path.insert(1, ROOT_FOLDER + '/')
django.setup()

#django imports
from django.conf import settings
from django.core.mail import EmailMessage

#local imports

#inter app imports
from payment.models import PaymentTxn
from shop.choices import DURATION_DICT,EXP_DICT
from order.models import Order,OrderItem,CouponOrder
from core.library.gcloud.custom_cloud_storage import GCPPrivateMediaStorage

#third party imports

def get_file_obj(file_name_suffix):
    file_name = "reports/discount_report_" + datetime.strftime(datetime.now(),"%Y_%m_%d") + \
             "_" + file_name_suffix + ".csv"
    
    if settings.IS_GCP:
        generated_file_obj = GCPPrivateMediaStorage().open(file_name, 'wb')
    else:
        generated_file_obj = open(settings.MEDIA_ROOT + '/' + file_name, 'w')
    return generated_file_obj


if __name__=="__main__":
    days_diff = int(sys.argv[1] if len(sys.argv) > 1 else 1)
    today = datetime.now()
    edt = datetime(today.year,today.month,today.day,0,0,0)
    sdt = edt - timedelta(days=days_diff)
    file_name_suffix = "daily" if days_diff == 1 else "monthly"
    file_obj = get_file_obj(file_name_suffix)

    csv_writer = csv.writer(file_obj, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(["order_id","Email","Owner_name","Order_Date","Payment_Date","Payment Time",\
                "Sales_executive","Sales_TL","Branch_Head","Transaction_ID","item_id","Product_Name",\
                "Item_Name","Experience","Course Duration","Status",\
                "Price of item on site according to order (without tax including context)",\
                "Discount (includes wallet and coupon)","Price of order with no discount/wallet",\
                "Actual collection of order","Effective collection per item",\
                "Price of item on site","Transaction_Amount","coupon_id","Payment_mode","Combo"])

    transactions = PaymentTxn.objects.filter(status=1,payment_date__gte=sdt,payment_date__lte=edt)
    order_ids = list(transactions.values_list('order_id',flat=True))
    orders = Order.objects.filter(status__in=[1,3],id__in=order_ids).order_by('id')
    logging.getLogger('info_log').info("Discount Report :: Total orders found - {}".format(orders.count()))

    for order in orders:
        order_items = OrderItem.objects.filter(order=order)
        try:
            sales_user_info = ast.literal_eval(order.sales_user_info)
        except:
            sales_user_info = {}
        txn_obj = order.get_txns().filter(status=1).first()
        coupon_order = CouponOrder.objects.filter(order=order).first()
        coupon_code = coupon_order.coupon_code if coupon_order else ""

        order_discount = sum(order_items.values_list('discount_amount',flat=True))
        order_cost_price = sum(order_items.values_list('cost_price',flat=True))
        order_selling_price = sum(order_items.values_list('selling_price',flat=True))
        price_without_wallet_discount = Decimal(order.total_incl_tax) + Decimal(order_discount * Decimal(1.18))

        for item in order_items:
            try:
                row_data = [
                    order.id,order.email,item.partner.name,order.date_placed.date(),\
                    txn_obj.payment_date.date(),txn_obj.payment_date.time(),sales_user_info.get('executive',''),\
                    sales_user_info.get('team_lead',''),sales_user_info.get('branch_head',''),\
                    txn_obj.txn,item.id,item.product.name,item.product.heading,\
                    EXP_DICT.get(item.product.get_exp(),"N/A"), \
                    DURATION_DICT.get(item.product.get_duration(),"N/A"),order.get_status,\
                    item.cost_price,order_discount,price_without_wallet_discount,order.total_incl_tax,\
                    item.selling_price,item.cost_price,order.total_incl_tax,\
                    coupon_code,txn_obj.get_payment_mode(),item.is_combo
                    ]

                csv_writer.writerow(row_data)

            except Exception as e:
                logging.getLogger('error_log').error("Discount Report | Order {} | {}".format(order.id,repr(e)))
                continue
    file_obj.close()


