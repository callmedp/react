#python imports
import logging
from decimal import Decimal
from datetime import datetime, timedelta
import ast,os,django,sys,subprocess,csv

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

#local imports

#inter app imports
from coupon.models import Coupon
from payment.models import PaymentTxn
from shop.choices import DURATION_DICT,EXP_DICT
from order.models import Order,OrderItem,CouponOrder, RefundItem
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
    csv_writer.writerow(["order_id","Candidate Id","Owner_name","Order_Date","Payment_Date","Payment Time",\
                "Last Payment Date","Last Payment Time","Sales_executive","Sales_TL",\
                "Branch_Head","Transaction_ID","item_id","Product Id","Product_Name",\
                "Item_Name","Experience","Course Duration","Status",\
                "Price of item on site according to order (without tax including context)",\
                "Discount (includes wallet and coupon)","Price of order with no discount/wallet",\
                "Actual collection of order","Effective collection per item",\
                "Delivery Service","Delivery Price Incl Tax","Delivery Price Excl Tax",\
                "Price of item on site","Transaction_Amount","coupon_id",\
                "Payment_mode","Combo", "Combo Parent","Variation","Refunded","Refund Amount",\
                "No Process", "Replaced", "Replaced With", "Replacement Of"])

    transactions = PaymentTxn.objects.filter(status=1,payment_date__gte=sdt,payment_date__lte=edt)
    order_ids = list(transactions.values_list('order_id',flat=True))
    orders = Order.objects.filter(status__in=[1,3],id__in=order_ids).order_by('id')
    logging.getLogger('info_log').info("\
        Discount Report :: Total orders found - {}".format(orders.count()))

    for order in orders:
        order_items = OrderItem.objects.filter(order=order)
        try:
            sales_user_info = ast.literal_eval(order.sales_user_info)
        except:
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
            combo_parent = False
            item_delivery_service = item.delivery_service.display_name if item.delivery_service else ""
            item_selling_price = item.selling_price
            item_cost_price = float(item.cost_price)
            if not item_cost_price:
                item_cost_price = float(item.product.inr_price)

            if item.product.type_product == 0 and item_selling_price == 0 \
                and not item.is_combo and not item.no_process: 
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
            if total_items == 1 and item_selling_price == 0:
                item_selling_price = float(float(order.total_excl_tax) - forced_coupon_amount)*1.18

            try:
                row_data = [
                    order.id,order.candidate_id,item.partner.name,order.date_placed.date(),\
                    txn_obj.payment_date.date(),txn_obj.payment_date.time(),\
                    last_txn_obj.payment_date.date(),last_txn_obj.payment_date.time(),\
                    sales_user_info.get('executive',''),\
                    sales_user_info.get('team_lead',''),sales_user_info.get('branch_head',''),\
                    transaction_ids,item.id,item.product.id,item.product.name,item.product.heading,\
                    EXP_DICT.get(item.product.get_exp(),"N/A"), \
                    DURATION_DICT.get(item.product.get_duration(),"N/A"),order.get_status,\
                    item_cost_price,order_discount,price_without_wallet_discount,order.total_incl_tax,\
                    float(item_selling_price)+float(item.delivery_price_incl_tax),item_delivery_service,item.delivery_price_incl_tax,\
                    item.delivery_price_excl_tax,item_cost_price,order.total_incl_tax,\
                    coupon_code,txn_obj.get_payment_mode(),item.is_combo, combo_parent,item.is_variation,\
                    bool(item_refund_request_list),refund_amount,item.no_process, replaced, replacement_id,\
                    order.replaced_order
                ]

                csv_writer.writerow(row_data)

            except Exception as e:
                logging.getLogger('error_log').error(\
                    "Discount Report | Order {} | {}".format(order.id,repr(e)))
                continue
    file_obj.close()


