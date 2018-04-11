from django.utils import timezone
from functools import reduce
from order.models import *
from django.db.models import Q
import datetime
import csv
import json
import re
from django.core.management.base import BaseCommand


def get_selling_price(oi):
    if oi.is_combo and not oi.no_process and oi.parent:
        return oi.cost_price*oi.parent.selling_price/sum(oi.parent.orderitem_set.filter(
            no_process=False, is_combo=True).values_list('cost_price',flat=True))
    elif oi.is_combo and oi.no_process:
        return 0
    else:
        return oi.selling_price + oi.delivery_price_incl_tax


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('start_date', nargs='+', type=str)
        parser.add_argument('end_date', nargs='+', type=str)

    def handle(self, *args, **options):
        start_date = datetime.datetime.strptime(options['start_date'][0], '%d/%m/%Y')
        end_date = datetime.datetime.strptime(options['end_date'][0], '%d/%m/%Y')
        csvfile = open('/tmp/report_finance.csv','w')
        filter_processes = Q(no_process=False)|Q(Q(is_combo=True)|~Q(product__product_class__slug__in=settings.COURSE_SLUG)&Q(no_process=True))
        writer=csv.writer(csvfile, delimiter=';')

        writer.writerow([
            'Order_Id','Email','Owner_name','Order_Date','Payment_Date','Sales_executive','Sales_TL', 'Branch_Head',
            'Transaction_ID', 'Item_Id', 'Product Name', 'Item Name','Status',
            'Price of item on site according to order (without tax including context)', 'Discount (includes wallet and coupon)',
            'Price of order with no discount/wallet', 'Actual collection of order', 'Effective collection per item',
            'Price of item on site ', 'Transaction_Amount', 'Coupon_Code', 'Payment_mode'])


        for oi in OrderItem.objects.filter(order__payment_date__gte=start_date,
        order__payment_date__lte=end_date,order__status__in=[1,2,3,4]).filter(filter_processes):

            discounts = reduce(lambda x, y: x + y, [x.discount_amount for x in oi.order.orderitems.filter(filter_processes)])
            fictitious_collection_with_no_discounts = ((oi.order.total_incl_tax/Decimal(1.18))+discounts)*Decimal(1.18)
            collection_after_discounts = oi.order.total_incl_tax
            c = re.sub("'", "\"", oi.order.sales_user_info)
            if c:
                c = json.loads(c)
            e = [
                oi.order.id,
                oi.order.email,
                oi.partner.name if oi.partner else '',
                oi.order.created,
                oi.order.payment_date,
                oi.order.crm_sales_id,
                c['team_lead'] if c else '',
                c['branch_head'] if c else '',
                '| '.join([tx.txn for tx in oi.order.get_txns()]),
                oi.id,
                oi.product.name,
                oi.parent.product.name if oi.parent else oi.product.name,
                oi.order.get_status_display(),
                oi.cost_price if not (oi.is_combo and not oi.no_process) else 0,
                discounts,
                fictitious_collection_with_no_discounts,
                collection_after_discounts,
                get_selling_price(oi),
                0 if (oi.is_combo and oi.no_process) else oi.cost_price,
                '| '.join([str(tx.txn_amount) for tx in oi.order.get_txns()]),
                '| '.join([str(o.coupon_code) for o in oi.order.couponorder_set.all()]),
                '| '.join([tx.get_payment_mode_display() for tx in oi.order.get_txns()])
            ]
            writer.writerow(e)


'''
SQL Dash Report

(
select
    details.order_id as Order_Id,
    details.email,
    details.Sales_executive,
    details.Sales_TL,
    details.Branch_Head,
    details.sales_user_info,
    details.Owner_name,
    details.Order_Date,
    details.Payment_Date,
    details.item_id as Item_Id,
    details.Type_flow as Type_flow,
    details.Item_Level as Item_Level,
    details.Item_Name as Item_Name,

    discinfo.GrossPrice_Order as GrossPrice_Order,
    discinfo.NetPrice_Order as NetPrice_Order,
    discinfo.NetDiscount as EffectiveDiscount_Order,

    details.Item_Price as NetPrice_Item,

    (((100-discinfo.NetDiscount)/100)*details.Item_Price) as EffectivePrice_Item,

    discinfo.CouponCode as Coupon_Code,
    discinfo.CouponDiscount as Coupon_Discount,
    discinfo.status as status,

    details.Transaction_ID,
    details.Transaction_Amount,
    details.Payment_mode

    from
        (
        select
            coi.order_id,
            replace(replace(replace(replace(substring_index(SUBSTRING_INDEX(co.sales_user_info, 'executive', -1),',',1),",",''),"'",""),"}",""),":","") as Sales_executive,
            replace(replace(replace(replace(SUBSTRING_INDEX(SUBSTRING_INDEX(co.sales_user_info, 'team_lead', -1),',',1),",",''),"'",""),"}",""),":","") as Sales_TL,
            replace(replace(replace(replace(SUBSTRING_INDEX(SUBSTRING_INDEX(co.sales_user_info, 'branch_head', -1),',',1),",",''),"'",""),"}",""),":","") as Branch_Head,
            sales_user_info,
            date(co.created) as Order_Date,
            date(co.payment_date) as Payment_Date,
            co.email as Email,
            coi.selling_price as Item_Price,
            coi.id as item_id,
            c_sp.type_flow as Type_flow,
            cp.name as Item_Level,
            pv.name as Owner_name,
            c_pp.Payment_mode,
            c_pp.Transaction_ID,
            c_pp.Transaction_Amount,
            IFNULL(cp_coi.name,cp.name) as Item_Name

            from

            careerplus.order_orderitem as coi

            left join

            careerplus.order_order as co
            on coi.order_id=co.id

            left join

            careerplus.shop_product as c_sp
            on c_sp.id=coi.product_id

            left join

            (
            select
                order_id,
                GROUP_CONCAT(txn ORDER BY txn ASC SEPARATOR ', ') as Transaction_ID,
                GROUP_CONCAT(
                    CASE
                    WHEN Payment_mode = '0' THEN 'Not Paid'
                    WHEN Payment_mode = '1' THEN 'Cash/Payment.Shine.com'
                    WHEN Payment_mode = '2' THEN 'Citrus_Pay'
                    WHEN Payment_mode = '3' THEN 'EMI'
                    WHEN Payment_mode = '4' THEN 'Cheque or Draft'
                    WHEN Payment_mode = '5' THEN 'CC-Avenue'
                    WHEN Payment_mode = '6' THEN 'Mobikwik'
                    WHEN Payment_mode = '7' THEN 'CC-Avenue-International'
                    WHEN Payment_mode = '8' THEN 'Debit Card'
                    WHEN Payment_mode = '9' THEN 'Credit Card'
                    WHEN Payment_mode = '10' THEN 'Net Banking'
                    END
                    ORDER BY txn ASC SEPARATOR ', ') as Payment_mode,
                GROUP_CONCAT(txn_amount ORDER BY txn ASC SEPARATOR ', ') as Transaction_Amount
                from
                careerplus.payment_paymenttxn
                group by order_id
            ) as c_pp
            on c_pp.order_id=co.id

            left join

            careerplus.shop_product as cp
            on coi.product_id=cp.id

            left join

            partner_vendor as pv
            on pv.id=cp.vendor_id

            left join

            (
            select
                coi_2.id,cp2.name from careerplus.order_orderitem as coi_2
                left join careerplus.order_orderitem as coi_3
                on coi_2.parent_id=coi_3.id
                left join careerplus.shop_product as cp2
                on cp2.id=coi_3.product_id
            ) as cp_coi
            on cp_coi.id=coi.id

            where date(co.payment_date) >= date_add(curdate(), interval -1 day)
            and co.status not in (0)
            order by 1 desc
        ) as details
        left join
        (
        select
            oi.order_id,
            oi.Items_Count as items,
            ed.GrossPrice_Order,
            ed.NetPrice_Order,
            ed.NetDiscount,
            oi.status,
            IFNULL(ed.coupon_id,'No Discount Coupon Offered') as CouponCode,
            IFNULL(ed.Coupon_Discount,'0') as CouponDiscount,
            if(ed.NetDiscount=0,'0',round((1-pow(((100-ed.NetDiscount)/100),1/(oi.Items_Count)))*100,0))as DistributedDiscount
            from
            (
                 #Calculating the number of items in each order
                 select coi.order_id,co.status,
                         count(*) as Items_Count
                 from careerplus.order_orderitem as coi
                 left join careerplus.order_order as co
                 on coi.order_id=co.id

                 where co.status not in (0)

                 group by 1
                 order by 1 desc
            ) as oi
            left join
            (
            #Getting effective discount for each order
            select
                co.id as order_id,
                op.GrossPrice_Order,
                co.TOTAL_INCL_TAX as NetPrice_Order,
                if(op.GrossPrice_Order-co.TOTAL_INCL_TAX=0,'NoDiscountOffered',round(((op.GrossPrice_Order-co.TOTAL_INCL_TAX)/op.GrossPrice_Order)*100,0))as NetDiscount,
                c_oc.coupon_id,
                cc.value as Coupon_Discount
                from careerplus.order_order as co
                left join (select order_id,sum(selling_price) as GrossPrice_Order from careerplus.order_orderitem group by 1) as op
                on co.id=op.order_id
                left join careerplus.order_couponorder as c_oc
                on c_oc.order_id = co.id
                left join careerplus.coupon_coupon as cc
                on c_oc.coupon_code=cc.code
                order by 1 desc
            ) as ed
             on oi.order_id=ed.order_id
             order by 1 desc
        ) as discinfo
    on details.order_id=discinfo.order_id
) as A




'''
