import logging
import datetime
import requests
from decimal import Decimal

from django.db.models import Sum, Count
from django.utils import timezone
from django.conf import settings
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser, )
from haystack import connections
from haystack.query import SearchQuerySet
from core.library.haystack.query import SQS
from partner.utils import CertiticateParser
from rest_framework.generics import ListAPIView
from oauth2_provider.contrib.rest_framework import OAuth2Authentication

from users.tasks import user_register
from order.models import Order, OrderItem, RefundRequest
from shop.views import ProductInformationMixin
from shop.models import Product
from coupon.models import Coupon, CouponUser
from core.api_mixin import ShineCandidateDetail
from payment.tasks import add_reward_point_in_wallet
from order.functions import update_initiat_orderitem_sataus
from geolocation.models import Country
from order.tasks import (
    pending_item_email,
    process_mailer,
    invoice_generation_order
)
from shop.models import Skill, DeliveryService, ShineProfileData

from .serializers import (
    OrderListHistorySerializer,
    RecommendedProductSerializer,
    RecommendedProductSerializerSolr,
    VendorCertificateSerializer,
    ImportCertificateSerializer,
    ShineDataFlowDataSerializer)
from shared.rest_addons.pagination import Learning_custom_pagination
from partner.models import Certificate

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
                    candidate_id, error = user_register(data)

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
                    coupon_code = request.data.get('coupon_code', '')
                    flag = False
                    if coupon_amount > 0 and coupon_code:
                        try:
                            coupon_obj = Coupon.objects.get(code=coupon_code)
                            order.couponorder_set.create(
                                coupon=coupon_obj,
                                coupon_code=coupon_obj.code,
                                value=coupon_amount
                            )
                            flag = True
                        except Exception as e:
                            logging.getLogger('error_log').error(str(e))

                    if coupon_amount > 0 and not flag:
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
                        delivery_service = None
                        parent_id = data.get('id')
                        addons = data.get('addons', [])
                        variations = data.get('variations', [])
                        combos = data.get('combos', [])
                        product = Product.objects.get(id=parent_id)
                        if data.get('delivery_service', None):
                            delivery_service = data.get('delivery_service', None)
                            delivery_service = DeliveryService.objects.get(name=delivery_service)

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
                                # setup delivery service
                                if delivery_service:
                                    oi.delivery_service = delivery_service
                                oi.save()

                        elif variations:
                            p_oi.is_variation = True
                            p_oi.no_process = True

                        cost_price = data.get('price')
                        p_oi.cost_price = cost_price
                        discount = (cost_price * percentage_discount) / 100
                        cost_price_after_discount = cost_price - discount
                        # As per product requirement , apply GST only for INR
                        if order.currency == 0:
                            tax_amount = (cost_price_after_discount * tax_rate_per) / 100
                        else:
                            tax_amount = 0
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

                        else:
                            if delivery_service:
                                # setup delivery service
                                p_oi.delivery_service = delivery_service

                                cost_price = float(p_oi.delivery_service.get_price())
                                p_oi.delivery_price_excl_tax = cost_price
                                discount = (cost_price * percentage_discount) / 100
                                cost_price_after_discount = cost_price - discount
                                # As per product requirement , apply GST only for INR
                                if order.currency == 0:
                                    tax_amount = (cost_price_after_discount * tax_rate_per) / 100
                                else:
                                    tax_amount = 0
                                selling_price = cost_price_after_discount + tax_amount
                                p_oi.delivery_price_incl_tax = selling_price
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
                            # As per product requirement , apply GST only for INR
                            if order.currency == 0:
                                tax_amount = (cost_price_after_discount * tax_rate_per) / 100
                            else:
                                tax_amount = 0
                            selling_price = cost_price_after_discount + tax_amount
                            oi.selling_price = selling_price
                            oi.tax_amount = tax_amount
                            oi.discount_amount = discount

                            # setup delivery service
                            if p_oi.product.product_class.slug == 'course':
                                if delivery_service:
                                    # setup delivery service
                                    p_oi.delivery_service = delivery_service

                                    cost_price = float(p_oi.delivery_service.get_price())
                                    p_oi.delivery_price_excl_tax = cost_price
                                    discount = (cost_price * percentage_discount) / 100
                                    cost_price_after_discount = cost_price - discount
                                    if order.currency == 0:
                                        tax_amount = (cost_price_after_discount * tax_rate_per) / 100
                                    else:
                                        tax_amount = 0
                                    selling_price = cost_price_after_discount + tax_amount
                                    p_oi.delivery_price_incl_tax = selling_price
                                    p_oi.save()
                            else:
                                if delivery_service:
                                    oi.delivery_service = delivery_service
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
                            # As per product requirement , apply GST only for INR
                            if order.currency == 0:
                                tax_amount = (cost_price_after_discount * tax_rate_per) / 100
                            else:
                                tax_amount = 0
                            selling_price = cost_price_after_discount + tax_amount
                            oi.selling_price = selling_price
                            oi.tax_amount = tax_amount
                            oi.discount_amount = discount
                            # setup delivery service
                            if delivery_service:
                                oi.delivery_service = delivery_service
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
        email = request.data.get('candidate_email', '').lower().strip()
        candidate_id = request.data.get('candidate_id')
        last_order = ""
        name = ''

        if not email and not candidate_id:
            return Response(
                {"status": "FAIL", "msg": "Bad Parameters Provided"},
                status=status.HTTP_400_BAD_REQUEST)

        ltv = Decimal(0)
        if not candidate_id:
            candidate_id = ShineCandidateDetail().get_shine_id(email=email)

        if not candidate_id:
            return Response(
                {"status": "FAIL", "msg": "Email or User Doesn't Exists"},
                status=status.HTTP_400_BAD_REQUEST)
        
        ltv_pks = list(Order.objects.filter(
            candidate_id=candidate_id,
            status__in=[1,2,3]).values_list('pk', flat=True))
        if ltv_pks:
            ltv_order_sum = Order.objects.filter(
                pk__in=ltv_pks).aggregate(ltv_price=Sum('total_incl_tax'))
            last_order = OrderItem.objects.select_related('order').filter(order__in = ltv_pks)\
                .exclude(oi_status=163).order_by('-order__payment_date').first()
            if last_order:
                last_order =last_order.order.payment_date.strftime('%Y-%m-%d %H:%M:%S')
            else:
                last_order=""

            ltv = ltv_order_sum.get('ltv_price') if ltv_order_sum.get('ltv_price') else Decimal(0)
            rf_ois = list(OrderItem.objects.filter(
                order__in=ltv_pks,
                oi_status=163).values_list('order', flat=True))

            rf_sum = RefundRequest.objects.filter(
                order__in=rf_ois).aggregate(rf_price=Sum('refund_amount'))
            if rf_sum.get('rf_price'):
                ltv = ltv - rf_sum.get('rf_price')

        return Response(
            {"status": "SUCCESS", "ltv_price": str(ltv), "name": name, "last_order": str(last_order)},
            status=status.HTTP_200_OK)
                            


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
                status__in=[1, 2, 3])
            return queryset_list
        elif email:
            queryset_list = queryset_list.filter(
                email=email,
                status__in=[1, 2, 3])
            return queryset_list


class ValidateCouponApiView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, format=None):
        coupon_code = request.data.get('coupon_code', '')
        crm_order_amount = request.data.get('order_amount', 0)
        lead_source = request.data.get('lead_source', 0)
        product_list = request.data.get('product_list', [])
        lead_mobile = request.data.get('lead_mobile', '')

        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
            except Exception as e:
                msg = str(e)
                logging.getLogger('error_log').error(msg)
                return Response({
                    "status": "FAIL",
                    "msg": 'This code is not valid.'},
                    status=status.HTTP_400_BAD_REQUEST)

            if coupon.is_redeemed:
                return Response({
                    "status": "FAIL",
                    "msg": 'This code has already been used.'},
                    status=status.HTTP_400_BAD_REQUEST)

            if coupon.expired():
                return Response({
                    "status": "FAIL",
                    "msg": 'This code is expired.'},
                    status=status.HTTP_400_BAD_REQUEST)

            if coupon.suspended():
                return Response({
                    "status": "FAIL",
                    "msg": 'This code is suspended.'},
                    status=status.HTTP_400_BAD_REQUEST)

            if coupon.site not in [0, 2]:
                return Response({
                    "status": "FAIL",
                    "msg": 'This code is not valid.'},
                    status=status.HTTP_400_BAD_REQUEST)

            if not coupon.is_valid_coupon(site=2, source=lead_source, cart_obj=None, product_list=product_list):
                if coupon.coupon_scope == 2:
                    error = 'This code is valid on particular sources.'
                elif coupon.coupon_scope == 1:
                    error = 'This code is valid on particular products.'

                return Response({
                    "status": "FAIL",
                    "msg": error},
                    status=status.HTTP_400_BAD_REQUEST)

            try:
                user_coupon = coupon.users.get(user=lead_mobile)
                if user_coupon.redeemed_at is not None:
                    return Response({
                        "status": "FAIL",
                        "msg": 'This code has already been used by your account.'},
                        status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logging.getLogger('error_log').error('unable to get coupon objects %s' % str(e))
                if coupon.user_limit is not 0:  # zero means no limit of user count
                    # only user bound coupons left and you don't have one
                    if coupon.user_limit is coupon.users.filter(user__isnull=False).count():
                        return Response({
                            "status": "FAIL",
                            "msg": 'This code is not valid for your account.'},
                            status=status.HTTP_400_BAD_REQUEST)

                    if coupon.user_limit is coupon.users.filter(redeemed_at__isnull=False).count():  # all coupons redeemed
                        return Response({
                            "status": "FAIL",
                            "msg": 'This code has already been used.'},
                            status=status.HTTP_400_BAD_REQUEST)

            try:
                total = Decimal(crm_order_amount)
                if coupon.min_purchase:
                    if total < coupon.min_purchase:
                        error = 'This cart total is below minimum purchase.(%s)' % (coupon.min_purchase)
                        return Response({
                            "status": "FAIL",
                            "msg": error},
                            status=status.HTTP_400_BAD_REQUEST)
                try:
                    coupon_user = coupon.users.get(user=lead_mobile)
                except CouponUser.DoesNotExist:
                    try:  # silently fix unbouned or nulled coupon users
                        coupon_user = coupon.users.get(user__isnull=True)
                        coupon_user.user = lead_mobile
                    except CouponUser.DoesNotExist:
                        coupon_user = CouponUser(coupon=coupon, user=lead_mobile)

                coupon_user.redeemed_at = timezone.now()
                coupon_user.save()
                discount_amount = 0
                if coupon.coupon_type == 'percent':
                    discount_amount = (total * coupon.value) / 100
                else:
                    discount_amount = coupon.value

                discount_amount = int(discount_amount)

                return Response({
                    "status": "SUCCESS",
                    "discount_amount": discount_amount,
                    "msg": 'Successfully Redeemed'},
                    status=status.HTTP_200_OK)

            except Exception as e:
                msg = str(e)
                logging.getLogger('error_log').error(msg)
                return Response({
                    "status": "FAIL",
                    "msg": 'Try after some Time'},
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "status": "FAIL",
                "msg": 'The coupon is not valid'},
                status=status.HTTP_400_BAD_REQUEST)


class RemoveCouponApiView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, format=None):
        try:
            coupon_code = request.data.get('coupon_code', '')
            user_mobile = request.data.get('lead_mobile', '')

            if coupon_code:
                coupon = None
                try:
                    coupon = Coupon.objects.get(code=coupon_code)
                except Exception as e:
                    msg = str(e)
                    logging.getLogger('error_log').error(msg)
                    return Response({
                        "status": "FAIL",
                        "msg": 'This code is not valid.'},
                        status=status.HTTP_400_BAD_REQUEST)

                if not coupon:
                    return Response({
                        "status": "FAIL",
                        "msg": 'No coupon is found.'},
                        status=status.HTTP_400_BAD_REQUEST)
                if not user_mobile:
                    return Response({
                        "status": "FAIL",
                        "msg": 'Coupon is not applied by this user'},
                        status=status.HTTP_400_BAD_REQUEST)
                try:
                    user_coupon = coupon.users.get(user=user_mobile)
                    user_coupon.redeemed_at = None
                    user_coupon.save()
                    return Response({
                        "status": "SUCCESS",
                        "msg": 'Coupon is removed successfully!'},
                        status=status.HTTP_200_OK)
                except CouponUser.DoesNotExist:
                    return Response({
                        "status": "SUCCESS",
                        "msg": 'Coupon is removed successfully!'},
                        status=status.HTTP_200_OK)
        except Exception as e:
            msg = str(e)
            logging.getLogger('error_log').error(msg)
        return Response({
            "status": "FAIL",
            "msg": 'Coupon code is not found!.'},
            status=status.HTTP_400_BAD_REQUEST)


class RecommendedProductsApiView(ListAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = RecommendedProductSerializerSolr
    pagination_class = Learning_custom_pagination

    def get_queryset(self, *args, **kwargs):
        skills = self.request.GET.get('skills', [])
        university_course = self.request.GET.get('uc', 0)
        prd_id = self.request.GET.get('product', None)
        if skills:
            skills = skills.split(',')
        products = SearchQuerySet().filter(
            pSkilln__in=skills,
            pPc=settings.COURSE_SLUG[0])
        if prd_id and prd_id.isdigit():
            products = products.exclude(id=int(prd_id))

        if university_course:
            products = products.filter(pTF=14)
        return products


class RecommendedProductsCategoryView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, *args, **kwargs):
        skills = self.request.GET.get('skills', '')
        res = {}
        haystack_conns = settings.HAYSTACK_CONNECTIONS.get(
            'default', {})

        solr_url = haystack_conns.get(
            'URL', 'http://10.136.2.25:8989/solr/prdt')

        url = '{}/select?defType=edismax&indent=on&\
        q={}&wt=json&qf=pHd^2%20pSkilln&group=true&group.field=pCtgs&\
        group.limit=5&rows=10&fq=pCtgs:[*%20TO%20*]&\
        fl=id,%20pHd,%20pBC,%20pImg,%20pURL,\
        %20pNJ,%20pRC,%20pARx,%20pSkilln,%20pCtgsD,%20pCtgs'.format(
            solr_url, skills)
        res = requests.get(url)
        return Response(
            res.json(),
            status=status.HTTP_200_OK)


from .tasks import cron_initiate
from .config import CRON_TO_ID_MAPPING


class CronInitiateApiView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        self.cron_id = self.kwargs.get('cron_id')
        if self.cron_id and int(self.cron_id) in CRON_TO_ID_MAPPING.keys():
            cron_initiate.delay(self.cron_id)
            return Response({
                "status": "SUCCESS",
                "msg": "Taks has been added, will notify you on your email after completion"},
                status=status.HTTP_200_OK
            )
        else:
            return Response({
                "status": "FAIL",
                "msg": 'Invalid cron id'},
                status=status.HTTP_400_BAD_REQUEST)


class RemoveCookieFromHeader(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        from django.http.response import HttpResponse
        response = HttpResponse()
        response.remove_cookie = True

        return response


class UpdateCertificateAndAssesment(APIView):

    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        vendor_name = self.kwargs.get('vendor_name')
        data = request.data
        data['vendor'] = vendor_name.lower()
        parser = CertiticateParser(parse_type=0)
        parsed_data = parser.parse_data(data)
        certificate, user_certificate = parser.save_parsed_data(parsed_data, vendor=data['vendor'])
        flag = parser.update_certificate_on_shine(user_certificate)
        if flag:
            logging.getLogger('info_log').error(
                "Certificate %s parsed, saved, updated for Candidate Id %s" %
                (str(certificate.name), str(user_certificate.candidate_id))
            )
        else:
            logging.getLogger('error_log').error(
                "Error Occured for Certificate %s for Candidate Id %s" %
                (str(certificate.name), str(user_certificate.candidate_id))
            )
        return Response({
            "status": 1,
            "msg": "Certificate Updated"},
            status=status.HTTP_201_CREATED
        )

class ShineDataFlowDataApiView(ListAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = ShineProfileData.objects.all()
    serializer_class = ShineDataFlowDataSerializer
    pagination_class = None



class VendorCertificateMappingApiView(ListAPIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Certificate.objects.all()
    serializer_class = VendorCertificateSerializer
    pagination_class = None


class ImportCertificateApiView(APIView):
    authentication_classes = []
    permission_classes = []

    def get_all_certiticate_data(self):

        data = {
            "status": "success",
            "code": 200,
            "data": {
                "certificates": [
                    {
                        "certificateName": "AMCAT Certified in C",
                        "skillValidated": "C",
                        "licenseNumber": "10017408486910-6",
                        "amcatID": 10017408486910,
                        "certificationDate": "2013-04-04 00:00:00",
                        "validTill": "2014-04-04"
                    },
                    {
                        "certificateName": "AMCAT Certified in Ms office",
                        "skillValidated": "Ms office",
                        "licenseNumber": "10017408486910-1",
                        "amcatID": 10017408486910,
                        "certificationDate": "2013-04-04 00:00:00",
                        "validTill": "2014-04-04"
                    },
                    {
                        "certificateName": "AMCAT Certified in Communication",
                        "skillValidated": "Communication",
                        "licenseNumber": "103541972-2",
                        "amcatID": 103541972,
                        "certificationDate": "2007-11-13 00:00:00",
                        "validTill": "2008-11-13"
                    },
                    {
                        "certificateName": "AMCAT Certified in Leadership Skills",
                        "skillValidated": "Leadership Skills",
                        "licenseNumber": "10014234777181-14",
                        "amcatID": 10014234777181,
                        "certificationDate": "2012-07-25 00:00:00",
                        "validTill": "2013-07-25"
                    }
                ],
                "scores": [
                    {
                        "overallScore": "123",
                        "testAttemptDate": "2007-11-13",
                        "amcatID": "103541972",
                        "modules": {
                            "5": {
                                "modulenames": "Computer Programming",
                                "mscores": 295,
                                "maxScores": 900
                            },
                            "693": {
                                "modulenames": "Basic computer literacy",
                                "mscores": 435,
                                "maxScores": 900
                            },
                            "972": {
                                "modulenames": "Effective Communication",
                                "mscores": 495,
                                "maxScores": 900
                            },
                            "2760": {
                                "modulenames": "WriteX",
                                "mscores": 475,
                                "maxScores": 900
                            }
                        }
                    },
                    {
                        "overallScore": "234",
                        "testAttemptDate": "2013-09-28",
                        "amcatID": "10018648902011",
                        "modules": {
                            "1": {
                                "modulenames": "English",
                                "mscores": 450,
                                "maxScores": 900
                            },
                            "5": {
                                "modulenames": "Computer Programming",
                                "mscores": 535,
                                "maxScores": 900
                            }
                        }
                    }
                ]
            },
            "message": None
        }

        return data

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '')
        vendor_name = self.kwargs.get('vendor_name')

        if not email:
            return Response({
                "status": 1,
                "msg": "Email is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        parser = CertiticateParser(parse_type=1)
        data = self.get_all_certiticate_data()
        data['vendor'] = vendor_name.lower()

        parsed_data = parser.parse_data(data)
        resp = {}
        certificates = ImportCertificateSerializer(
            parsed_data.certificates,
            many=True,
            context={'vendor_provider': vendor_name}
        )
        resp['count'] = len(certificates.data)
        resp['results'] = certificates.data
        return Response(resp, status=status.HTTP_200_OK)
