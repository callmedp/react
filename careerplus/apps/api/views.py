import logging
import datetime
from decimal import Decimal
from django.db.models import Sum
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser, )
from rest_framework.generics import ListAPIView
from oauth2_provider.contrib.rest_framework import OAuth2Authentication

from users.tasks import user_register
from order.models import Order, OrderItem, RefundRequest
from shop.views import ProductInformationMixin
from shop.models import Product
from coupon.models import Coupon
from core.api_mixin import ShineCandidateDetail
from .serializers import OrderListHistorySerializer
from payment.tasks import add_reward_point_in_wallet
from order.functions import update_initiat_orderitem_sataus
from geolocation.models import Country
from order.tasks import (
    pending_item_email,
    process_mailer,
    invoice_generation_order
)


class CreateOrderApiView(APIView, ProductInformationMixin):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, format=None):
        item_list = request.data.get('item_list', [])
        name = request.data.get('name', '').strip()
        email = request.data.get('email', '').strip()
        country_code = request.data.get('country_code', '91').strip()
        mobile = request.data.get('mobile').strip()
        candidate_id = request.data.get('candidate_id', '').strip()
        if item_list:
            try:
                order = None
                flag = True
                msg = ''
                if not email and flag:
                    msg = 'email is required.'
                    flag = False
                elif not mobile and flag:
                    msg = 'mobile number is required.'
                    flag = False

                if email and not candidate_id:
                    data = {
                        "email": email,
                        "country_code": country_code,
                        "cell_phone": mobile,
                        "name": name,
                    }
                    candidate_id = user_register(data)

                if not candidate_id and flag:
                    msg = 'candidate_id is required.'
                    flag = False

                first_name, last_name = '', ''

                if candidate_id:
                    status_response = ShineCandidateDetail().get_status_detail(
                        email=None, shine_id=candidate_id)

                    if status_response:
                        first_name = status_response.get('first_name')
                        last_name = status_response.get('last_name')

                    if not first_name and not last_name:
                        first_name = name

                if country_code:
                    try:
                        country_obj = Country.objects.get(phone=country_code)
                    except Exception as e:
                        logging.getLogger('error_log').error("Unable to get country object %s" % str(e))

                        country_obj = Country.objects.get(phone=91)

                if flag:
                    percentage_discount = 0
                    tax_rate_per = int(request.data.get('tax_rate_per', 0))
                    order = Order.objects.create(
                        candidate_id=candidate_id,
                        email=email,
                        country_code=country_code,
                        mobile=mobile,
                        date_placed=timezone.now(),
                        payment_date=timezone.now())

                    order.number = 'CP' + str(order.id)
                    order.first_name = first_name
                    order.last_name = last_name
                    order.currency = int(request.data.get('currency', 0))
                    order.tax_config = str(request.data.get('tax_config', {}))
                    order.status = 1
                    order.site = 1
                    order.country = country_obj
                    order.total_excl_tax = request.data.get('total_excl_tax_excl_discount', 0)
                    order.total_incl_tax = request.data.get('total_payable_amount', 0)
                    crm_lead_id = request.data.get('crm_lead_id', '')
                    crm_sales_id = request.data.get('crm_sales_id', '')
                    sales_user_info = request.data.get('sales_user_info', {})
                    sales_user_info = str(sales_user_info)
                    order.crm_lead_id = crm_lead_id
                    order.crm_sales_id = crm_sales_id
                    order.sales_user_info = sales_user_info
                    order.save()
                    coupon_amount = request.data.get('coupon', 0)
                    if coupon_amount > 0:
                        coupon_obj = Coupon.objects.create_coupon(
                            coupon_type='flat',
                            value=coupon_amount,
                            valid_until=None,
                            prefix="crm",
                            campaign=None,
                            user_limit=1
                        )

                        coupon_obj.min_purchase = coupon_amount
                        coupon_obj.max_deduction = coupon_amount
                        coupon_obj.valid_from = timezone.now()
                        coupon_obj.valid_until = timezone.now()
                        coupon_obj.active = False
                        coupon_obj.save()

                        coupon_obj.users.create(
                            user=email,
                            redeemed_at=timezone.now()
                        )

                        order.couponorder_set.create(
                            coupon=coupon_obj,
                            coupon_code=coupon_obj.code,
                            value=coupon_amount
                        )

                        total_discount = coupon_amount
                        total_amount_before_discount = order.total_excl_tax  # berfore discount and excl tax

                        percentage_discount = (total_discount * 100) / total_amount_before_discount

                    for data in item_list:
                        parent_id = data.get('id')
                        addons = data.get('addons', [])
                        variations = data.get('variations', [])
                        combos = data.get('combos', [])
                        product = Product.objects.get(id=parent_id)

                        p_oi = order.orderitems.create(
                            product=product,
                            title=product.get_name,
                            partner=product.vendor
                        )
                        p_oi.upc = str(order.pk) + "_" + str(p_oi.pk)
                        if product.type_flow == 8:
                            p_oi.oi_status = 2
                        if product.type_product == 3:
                            p_oi.is_combo = True
                            p_oi.no_process = True
                            combos = self.get_combos(product).get('combos')
                            for prd in combos:
                                oi = order.orderitems.create(
                                    product=prd,
                                    title=prd.get_name,
                                    partner=prd.vendor,
                                    parent=p_oi,
                                    is_combo=True
                                )
                                if prd.type_flow == 8:  # Linkedin Orders Resume required status
                                    oi.oi_status = 2
                                oi.upc = str(order.pk) + "_" + str(oi.pk)
                                cost_price = oi.product.get_price()
                                oi.cost_price = cost_price
                                oi.selling_price = 0
                                oi.tax_amount = 0
                                oi.discount_amount = 0
                                oi.save()

                        elif variations:
                            p_oi.is_variation = True
                            p_oi.no_process = True

                        cost_price = data.get('price')
                        p_oi.cost_price = cost_price
                        discount = (cost_price * percentage_discount) / 100
                        cost_price_after_discount = cost_price - discount
                        tax_amount = (cost_price_after_discount * tax_rate_per) / 100
                        selling_price = cost_price_after_discount + tax_amount
                        p_oi.selling_price = selling_price
                        p_oi.tax_amount = tax_amount
                        p_oi.discount_amount = discount
                        p_oi.save()

                        if variations and p_oi.product.product_class.slug == 'course':
                            p_oi.selling_price = 0
                            p_oi.tax_amount = 0
                            p_oi.discount_amount = 0
                            p_oi.save()

                        for var in variations:
                            prd = Product.objects.get(id=var.get('id'))
                            oi = order.orderitems.create(
                                product=prd,
                                title=prd.get_name,
                                partner=prd.vendor,
                                parent=p_oi,
                                is_variation=True,
                            )
                            if prd.type_flow == 8:  # Linkedin Orders Resume required status
                                oi.oi_status = 2
                            oi.upc = str(order.pk) + "_" + str(oi.pk)
                            cost_price = var.get('price')
                            oi.cost_price = cost_price
                            discount = (cost_price * percentage_discount) / 100
                            cost_price_after_discount = cost_price - discount
                            tax_amount = (cost_price_after_discount * tax_rate_per) / 100
                            selling_price = cost_price_after_discount + tax_amount
                            oi.selling_price = selling_price
                            oi.tax_amount = tax_amount
                            oi.discount_amount = discount
                            oi.save()

                        for addon in addons:
                            prd = Product.objects.get(id=addon.get('id'))
                            oi = order.orderitems.create(
                                product=prd,
                                title=prd.get_name,
                                partner=prd.vendor,
                                parent=p_oi,
                                is_addon=True,
                            )
                            if prd.type_flow == 8:  # Linkedin Orders Resume required status
                                oi.oi_status = 2
                            oi.upc = str(order.pk) + "_" + str(oi.pk)
                            cost_price = addon.get('price')
                            oi.cost_price = cost_price
                            discount = (cost_price * percentage_discount) / 100
                            cost_price_after_discount = cost_price - discount
                            tax_amount = (cost_price_after_discount * tax_rate_per) / 100
                            selling_price = cost_price_after_discount + tax_amount
                            oi.selling_price = selling_price
                            oi.tax_amount = tax_amount
                            oi.discount_amount = discount
                            oi.save()

                    update_initiat_orderitem_sataus(order=order)
                    txns_list = request.data.get('txns_list', [])

                    for txn_dict in txns_list:
                        try:
                            payment_date = txn_dict.get('payment_date')
                            payment_date = datetime.datetime.strptime(payment_date, "%Y-%m-%d %H:%M:%S")
                        except Exception as e:
                            logging.getLogger('error_log').error("Unable to get payment date as per specified format "
                                                                 "%s" %
                                                                 str(e))
                            payment_date = timezone.now()
                        order.ordertxns.create(
                            txn=txn_dict.get('txn_id', ''),
                            status=int(txn_dict.get('status', 0)),
                            payment_mode=int(txn_dict.get('payment_mode', 7)),
                            payment_date=payment_date,
                            currency=int(txn_dict.get('currency', 0)),
                            txn_amount=txn_dict.get('amount', 0)
                        )

                    # wallet reward point
                    # OrderMixin().addRewardPointInWallet(order=order)
                    add_reward_point_in_wallet.delay(order_pk=order.pk)

                    # invoice generation
                    invoice_generation_order.delay(order_pk=order.pk)

                    # email for order
                    process_mailer.apply_async((order.pk,), countdown=900)
                    pending_item_email.apply_async((order.pk,), countdown=900)

                    return Response(
                        {"status": 1, "msg": 'order created successfully.'},
                        status=status.HTTP_200_OK)

                else:
                    return Response(
                        {"msg": msg, "status": 0},
                        status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                if order:
                    order.delete()
                msg = str(e)
                logging.getLogger('error_log').error(msg)
                return Response(
                    {"msg": msg, "status": 0},
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"status": 0, "msg": "there is no items in order"},
                status=status.HTTP_400_BAD_REQUEST)


class EmailLTValueApiView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, format=None):
        email = request.data.get('candidate_email', '')
        c_id = request.data.get('candidate_id', '')
        name = ''
        candidate_id = None
        if email or c_id:
            ltv = Decimal(0)
            if not c_id:
                email = email.lower().strip()
                candidate_response = ShineCandidateDetail().get_candidate_detail(email=email)
                if candidate_response:
                    personal_detail = candidate_response.get('personal_detail')[0] if candidate_response.get('personal_detail') else None
                    if personal_detail:
                        candidate_id = personal_detail.get('id')
                        name = personal_detail.get('first_name', '') + ' ' + personal_detail.get('last_name', '')  
            else:
                candidate_id = c_id
            if candidate_id:
                ltv_pks = Order.objects.filter(
                    candidate_id=candidate_id,
                    status__in=[1,2,3]).values_list('pk', flat=True)
                if ltv_pks:
                    ltv_order_sum = Order.objects.filter(
                        pk__in=ltv_pks).aggregate(ltv_price=Sum('total_incl_tax'))
                    ltv = ltv_order_sum.get('ltv_price') if ltv_order_sum.get('ltv_price') else Decimal(0)
                    rf_ois = OrderItem.objects.filter(
                        order__in=ltv_pks,
                        oi_status=163).values_list('order', flat=True)
                    rf_sum = RefundRequest.objects.filter(
                        order__in=rf_ois).aggregate(rf_price=Sum('refund_amount'))
                    if rf_sum.get('rf_price'):
                        ltv = ltv - rf_sum.get('rf_price')

                return Response(
                    {"status": "SUCCESS", "ltv_price": str(ltv), "name": name},
                    status=status.HTTP_200_OK)
            else:
                return Response(
                    {"status": "FAIL", "msg": "Email or User Doesn't Exists"},
                    status=status.HTTP_400_BAD_REQUEST)    
        else:
            return Response(
                {"status": "FAIL", "msg": "Bad Parameters Provided"},
                status=status.HTTP_400_BAD_REQUEST)


class OrderHistoryAPIView(ListAPIView):
    serializer_class = OrderListHistorySerializer
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    # permission_classes = []

    def get_queryset(self, *args, **kwargs):
        email = self.request.GET.get("email", None)
        candidate_id = self.request.GET.get("candidate_id", None)
        queryset_list = Order.objects.all()
        if not email and not candidate_id:
            return queryset_list.none()
        elif candidate_id:
            queryset_list = queryset_list.filter(
                candidate_id=candidate_id,
                status__in=[1, 2, 3]).distinct()
            return queryset_list
        elif email:
            queryset_list = queryset_list.filter(
                email=email,
                status__in=[1, 2, 3]).distinct()
            return queryset_list
