import logging, binascii, os, pickle
import datetime

import requests
from decimal import Decimal
from datetime import timedelta
from django.db.models import Sum, Count, Subquery, OuterRef, F
from django.utils import timezone
from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser, )

from rest_framework.generics import ListAPIView, CreateAPIView,RetrieveAPIView
from rest_framework.authentication import SessionAuthentication
from haystack import connections
from haystack.query import SearchQuerySet
from core.library.haystack.query import SQS
from partner.utils import CertiticateParser
from partner.models import ProductSkill
from rest_framework.generics import ListAPIView, RetrieveAPIView
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from django_filters.rest_framework import DjangoFilterBackend

from users.tasks import user_register
from order.models import Order, OrderItem, RefundRequest
from order.utils import get_ltv
from shop.views import ProductInformationMixin
from shop.models import Product, Category
from coupon.models import Coupon, CouponUser
from core.api_mixin import ShineCandidateDetail, AmcatApiMixin
from payment.tasks import add_reward_point_in_wallet
from order.functions import update_initiat_orderitem_sataus
from geolocation.models import Country
from order.tasks import (
    pending_item_email,
    process_mailer,
    invoice_generation_order
)
from shop.models import Skill, DeliveryService, ShineProfileData
from blog.models import Blog
from emailers.tasks import send_email_task
from payment.models import PaymentTxn
from resumebuilder.models import Candidate 

from .serializers import (
    OrderListHistorySerializer,
    RecommendedProductSerializer,
    RecommendedProductSerializerSolr,
    MediaUploadSerializer,
    ResumeBuilderProductSerializer,
    ShineDataFlowDataSerializer,
    VendorCertificateSerializer,
    ImportCertificateSerializer,
    ShineDataFlowDataSerializer,
    CertificateSerializer,TalentEconomySerializer,QuestionAnswerSerializer,
    OrderDetailSerializer, OrderListSerializer)

from partner.models import Certificate, Vendor
from shared.rest_addons.pagination import LearningCustomPagination

from shared.rest_addons.permissions import OrderAccessPermission
from shared.rest_addons.authentication import ShineUserAuthentication
from shared.rest_addons.mixins import (SerializerFieldsMixin, FieldFilterMixin)

from django_redis import get_redis_connection
from shared.utils import ShineCandidate
from linkedin.autologin import AutoLogin
from users.mixins import RegistrationLoginApi
from .education_specialization import educ_list
from assessment.models import Question
from assessment.utils import TestCacheUtil


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

        if not item_list:
            return Response(
                {"status": 0, "msg": "there is no items in order"},
                status=status.HTTP_400_BAD_REQUEST)

        txns_list = request.data.get('txns_list', [])
        order_already_created = False

        all_txn_ids = [x['txn_id'] for x in txns_list if x.get('txn_id')]
        paid_transactions = PaymentTxn.objects.filter(txn__in=all_txn_ids,status=1)

        if paid_transactions:
            logging.getLogger("error_log").error("Order for txns already created. {}".format(all_txn_ids))
            return Response({"status": 0, "msg": "Order for txns already created."},
                status=status.HTTP_400_BAD_REQUEST)

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
                process_mailer.apply_async((order.pk,), countdown=settings.MAIL_COUNTDOWN)
                pending_item_email.apply_async((order.pk,), countdown=settings.MAIL_COUNTDOWN)

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

        if not candidate_id:
            candidate_id = ShineCandidateDetail().get_shine_id(email=email)

        if not candidate_id:
            return Response(
                {"status": "FAIL", "msg": "Email or User Doesn't Exists"},
                status=status.HTTP_400_BAD_REQUEST)

        ltv = get_ltv(candidate_id)

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

                    if coupon.user_limit is coupon.users.filter(
                            redeemed_at__isnull=False).count():  # all coupons redeemed
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
    pagination_class = LearningCustomPagination

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


from .tasks import cron_initiate, create_assignment_lead
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


class MediaUploadView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = MediaUploadSerializer


class ResumeBuilderProductView(ListAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ResumeBuilderProductSerializer

    def get_queryset(self):
        type_flow = self.request.query_params.get('type_flow')
        product_list = Product.objects.filter(type_flow=type_flow, type_product=0, active=True, sub_type_flow='1701').values('id', 'name', 'inr_price', 'usd_price', 'aed_price').order_by('inr_price')

        # for item in  product_list:
        #     product = Product.objects.filter(id=item['id']).first()
        #     value = product.attr.get_value_by_attribute(product.attr.get_attribute_by_name('template_type')).value or '';
        #     if( value == 'single' or value == 'multiple'):
        #         new_product_list.append(item)
        return product_list

class ShineDataFlowDataApiView(ListAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = ShineProfileData.objects.all()
    serializer_class = ShineDataFlowDataSerializer
    pagination_class = None


class ShineCandidateLoginAPIView(APIView):
    """
    Sample Input Data - <br><br>
    {
        "email":"sharma.animesh@hotmail.com",
        "password":"1234",
        "alt":"CwcWCBUDCwlIVk8hHwsZCBRIGw4VGk1SHgBJAklXS1RIAkEFSQBMUBkEGQMeAgRTSFdBUUxUSFNIVU9VTxoABwAH"
    }
    Constraints - <br><br>
    Required - email/password or alt
    """
    serializer_class = None
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = ()
    conn = get_redis_connection('token')

    def set_user_in_cache(self, token, candidate_obj):
        self.conn.set(candidate_obj.id, pickle.dumps(token))
        self.conn.set(token, pickle.dumps(candidate_obj))

    def generate_token(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def get_or_create_token(self, candidate_obj):
        existing_token = self.conn.get(candidate_obj.id)
        token = pickle.loads(existing_token) if existing_token else self.generate_token()
        self.set_user_in_cache(token, candidate_obj)
        return token

    def get_entity_status_for_candidate(self, candidate_id, BUILDER_ENTITY_MAPPING=None):
        from resumebuilder.models import Candidate, Skill, CandidateExperience, \
            CandidateEducation, CandidateCertification, CandidateProject, \
            CandidateReference, CandidateSocialLink, CandidateLanguage, CandidateAchievement

        from resumebuilder.choices import BUILDER_ENTITY_KEYS
        entity_mapping = dict(BUILDER_ENTITY_KEYS)

        entity_slug_model_mapping = {1: (Candidate, "candidate_id"),
                                     2: (Skill, "candidate__candidate_id"),
                                     3: (CandidateExperience, "candidate__candidate_id"),
                                     4: (CandidateEducation, "candidate__candidate_id"),
                                     5: (CandidateCertification, "candidate__candidate_id"),
                                     6: (CandidateProject, "candidate__candidate_id"),
                                     7: (CandidateReference, "candidate__candidate_id"),
                                     # 8: (CandidateSocialLink, "candidate__candidate_id"),
                                     8: (CandidateLanguage, "candidate__candidate_id"),
                                     9: (CandidateAchievement, "candidate__candidate_id")
                                     }

        data = []
        for key, value_tuple in entity_slug_model_mapping.items():
            model = value_tuple[0]
            objects_count = model.objects.filter(**{value_tuple[1]: candidate_id}).count()
            d = {"id": key, "set": bool(objects_count), "display_value": entity_mapping.get(key)}
            data.append(d)

        return data

    def get_existing_order_data(self, candidate_id):
        from order.models import Order

        product_found = False
        order_data = {}
        order_obj_list = Order.objects.filter(candidate_id=candidate_id, status__in=[1, 3])

        if not order_obj_list:
            return order_data

        for order_obj in order_obj_list:
            if product_found:
                break

            for item in order_obj.orderitems.all():
                if item.product and item.product.type_flow == 17 and item.product.type_product == 0:
                    order_data = {"id": order_obj.id,
                                  "combo": True if item.product.attr.get_value_by_attribute(item.product.attr.get_attribute_by_name('template_type')).value == 'multiple' else False
                                  }
                    product_found = True
                    break

        return order_data

    def get_candidate_experience(self,login_response):
        return (login_response['workex'] and login_response['workex'][0] and login_response['workex'][0].get('experience_in_years',0)) or 0

    def get_response_for_successful_login(self, candidate_id, login_response, with_info=True):
        candidate_obj = ShineCandidate(**login_response)
        candidate_obj.id = candidate_id
        candidate_obj.candidate_id = candidate_id
        token = self.get_or_create_token(candidate_obj)
        personal_info = login_response.get('personal_detail')[0]
        personal_info['candidate_id']= personal_info.get('id')
        subscription_active = False
        # Check whether subscription active or not if resumebuilder candidate exists 
        resumebuilder_candidate = Candidate.objects.filter(candidate_id=candidate_id).first()
        if resumebuilder_candidate:
            subscription_active = resumebuilder_candidate.active_subscription or False

        self.request.session.update(login_response)
        
        self.request.session.update(personal_info)

        if with_info:
            data_to_send = {"token": token,
                            "candidate_id": candidate_id,
                            "candidate_profile": self.customize_user_profile(login_response),
                            "entity_status": self.get_entity_status_for_candidate(candidate_id),
                            "order_data": self.get_existing_order_data(candidate_id),
                            "userExperience": self.get_candidate_experience(login_response),
                            "subscription_active": subscription_active
                            # TODO make param configurable
                            }
        else:
            data_to_send = {
                "token": token,
                "candidate_id": candidate_id,
                'cart_pk': self.request.session.get('cart_pk') or self.request._request.session.get('cart_pk'),
                'profile': personal_info
            }

        return Response(data_to_send, status=status.HTTP_201_CREATED)

    def get_profile_info(self, profile):
        candidate_profile_keys = ['first_name', 'last_name', 'email', 'number', 'date_of_birth', 'location', 'gender',
                                  'candidate_id']
        candidate_profile_values = [profile.get('first_name',''), profile.get('last_name', ''), profile.get('email',''),
                                    profile.get('cell_phone',''), profile.get('date_of_birth',''),
                                    profile.get('candidate_location',''), profile.get('gender',''), profile.get('id','')]
        candidate_profile = dict(zip(candidate_profile_keys, candidate_profile_values))

        return candidate_profile

    def get_education_info(self, education):
        candidate_education_keys = ['candidate_id', 'specialization', 'institution_name', 'course_type',
                                    'percentage_cgpa',
                                    'start_date',
                                    'end_date', 'is_pursuing', 'order']
        candidate_education = []

        for ind, edu in enumerate(education):
            course_type = ""
            if edu['course_type'] == 1:
                course_type = "FT"
            elif edu['course_type'] == 2:
                course_type = "PT"
            else:
                course_type = "CR"

            degree_index = next((index for (index, d) in enumerate(educ_list) if d["pid"] == edu['education_level']),
                                None)

            degree_name = educ_list[degree_index]['pdesc'];

            child = educ_list[degree_index]['child']

            specialization_index = next((index for (index, d) in enumerate(child)
                                         if d['cid'] == edu['education_specialization']), None)
            specialization_name = child[specialization_index]['cdesc']

            candidate_education_values = ['', '{}({})'.format(degree_name, specialization_name),
                                          edu['institute_name'],
                                          course_type,
                                          '',
                                          None, None, True, ind]
            education_dict = dict(zip(candidate_education_keys, candidate_education_values))
            candidate_education.append(education_dict)

        return candidate_education

    def get_experience_info(self, experience):
        candidate_experience_keys = ['candidate_id', 'job_profile', 'company_name', 'start_date', 'end_date',
                                     'is_working', 'job_location', 'work_description', 'order']
        candidate_experience = []

        for ind, exp in enumerate(experience):
            start_date = datetime.datetime.strptime(exp['start_date'], '%Y-%m-%dT%H:%M:%S').date() \
                if exp['start_date'] is not None else \
                exp['start_date']
            end_date = datetime.datetime.strptime(exp['end_date'], '%Y-%m-%dT%H:%M:%S').date() \
                if exp['end_date'] is not None else \
                exp['end_date']
            candidate_experience_values = ['', exp['job_title'], exp['company_name'],
                                           start_date, end_date,
                                           exp['is_current'], '', exp['description'], ind]
            experience_dict = dict(zip(candidate_experience_keys, candidate_experience_values))
            candidate_experience.append(experience_dict)

        return candidate_experience

    def get_skill_info(self, skills):
        skill_keys = ['candidate_id', 'name', 'proficiency', 'order']
        candidate_skill = []

        for ind, skill in enumerate(skills):
            candidate_skill_values = ['', skill['value'], 5, ind]
            skill_dict = dict(zip(skill_keys, candidate_skill_values))
            candidate_skill.append(skill_dict)

        return candidate_skill

    def get_certification_info(self, certifications):
        candidate_certification_keys = ['candidate_id', 'name_of_certification', 'year_of_certification', 'order']
        candidate_certification = []

        for ind, certi in enumerate(certifications):
            candidate_certification_values = ['', certi['certification_name'], certi['certification_year'], ind]
            certification_dict = dict(zip(candidate_certification_keys, candidate_certification_values))
            candidate_certification.append(certification_dict)

        if len(candidate_certification) == 0:
            candidate_certification = [{
                "candidate_id": '',
                "id": '',
                "name_of_certification": '',
                "year_of_certification": '',
                "order": 0
            }]
            return candidate_certification

    def customize_user_profile(self, login_response):

        # get personal info
        profile = login_response and login_response['personal_detail'][0]
        candidate_info = dict()
        candidate_info['personalInfo'] = self.get_profile_info(profile)

        # get education info
        candidate_info['education'] = self.get_education_info(login_response and login_response['education'])

        #  get experience info
        candidate_info['experience'] = self.get_experience_info(login_response and login_response['jobs'])

        #  get skills
        candidate_info['skill'] = self.get_skill_info(login_response and login_response['skills'])

        #  get language
        candidate_info['language'] = [{
            "candidate_id": '',
            "id": '',
            "name": '',
            "proficiency": {
                'value': 5, 'label': '5'
            },
            'order': 0
        }]

        #  get courses
        candidate_info['course'] = self.get_certification_info(login_response and login_response['certifications'])

        #   get award
        candidate_info['award'] = [{
            "candidate_id": '',
            "id": '',
            "title": '',
            "date": '',
            "summary": '',
            "order": 0
        }]

        #  get reference
        candidate_info['reference'] = [{
            "candidate_id": '',
            "id": '',
            "reference_name": '',
            "reference_designation": '',
            "about_user": "",
            "order": 0
        }]

        #  get projects
        candidate_info['project'] = [{
            "candidate_id": '',
            "id": '',
            "project_name": '',
            "start_date": '',
            "end_date": '',
            "skills": [],
            "description": '',
            "order": 0
        }]

        return candidate_info

    def _dispatch_via_autologin(self, alt, with_info):
        try:
            alt = alt.replace(" ","+")
            alt = alt.replace("%20","+")
            email, candidate_id, valid = AutoLogin().decode(alt)
        except Exception as e:
            logging.getLogger('error_log').error("Login attempt failed - {}".format(e))
            return Response({"data": "No user record found"}, status=status.HTTP_400_BAD_REQUEST)

        if not valid or not candidate_id:
            return Response({"data": "No user record found"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            login_response = ShineCandidateDetail().get_candidate_detail(shine_id=candidate_id)
        except Exception as e:
            logging.getLogger('error_log').error("Login attempt failed - {}".format(e))
            return Response({"data": "No user record found"}, status=status.HTTP_400_BAD_REQUEST)

        return self.get_response_for_successful_login(candidate_id, login_response, with_info)

    def _dispatch_via_email_password(self, email, password, with_info):
        login_data = {"email": email.strip(), "password": password}

        try:
            login_resp = RegistrationLoginApi.user_login(login_data)
        except Exception as e:
            logging.getLogger('error_log').error("Login attempt failed - {}".format(e))
            return Response({"data": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        candidate_id = login_resp.get('candidate_id')
        access_token = login_resp.get('access_token')

        if not candidate_id and not access_token:
            logging.getLogger('info_log').info("Login attempt failed - {}".format(login_resp))
            return Response({"data": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            login_response = ShineCandidateDetail().get_candidate_detail(shine_id=candidate_id)
            # else:
            #     login_response = ShineCandidateDetail().get_status_detail(shine_id=candidate_id)
        except Exception as e:
            logging.getLogger('error_log').error("Login attempt failed - {}".format(e))
            return Response({"data": "No user record found"}, status=status.HTTP_400_BAD_REQUEST)

        return self.get_response_for_successful_login(candidate_id, login_response, with_info)

    def get(self, request, *args, **kwargs):
        user = request.user
        candidate_id = request.session.get('candidate_id')
        if not user.is_authenticated() and not candidate_id:
            return Response({"detail": "Not Authorised"}, status=status.HTTP_401_UNAUTHORIZED)

        if not candidate_id:
            candidate_id = user.candidate_id

        try:
            login_response = ShineCandidateDetail().get_candidate_detail(shine_id=candidate_id)
        except Exception as e:
            logging.getLogger('error_log').error("Login attempt failed - {}".format(e))
            return Response({"data": "No user record found"}, status=status.HTTP_400_BAD_REQUEST)

        return self.get_response_for_successful_login(candidate_id, login_response)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        alt = request.data.get('alt')
        with_info = request.data.get('withInfo', True)

        if alt:
            return self._dispatch_via_autologin(alt, with_info)

        if email and password:
            return self._dispatch_via_email_password(email, password, with_info)

        return Response({"data": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class UpdateCertificateAndAssesment(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        certificate_updated = False
        subject = "Sorry, You have not cleared the test."
        vendor_name = self.kwargs.get('vendor_name')
        data = request.data
        logging.getLogger('info_log').error(
            "Incoming Data in request is %s" %
            str(data)
        )
        if not data:
            return Response({
                "status": 0,
                "msg": "Provide Data for Certificate"},
                status=status.HTTP_400_BAD_REQUEST
            )

        data['vendor'] = vendor_name.lower()
        parser = CertiticateParser(parse_type=0)
        parsed_data = parser.parse_data(data)
        certificates, user_certificates = parser.save_parsed_data(parsed_data, vendor=data['vendor'])
        if user_certificates:
            for user_certificate in user_certificates:
                certificate = user_certificate.certificate
                flag = parser.update_certificate_on_shine(user_certificate)

                if flag:
                    certificate_updated = True
                    logging.getLogger('info_log').info(
                        "Certificate %s parsed, saved, updated for Candidate Id %s" %
                        (str(certificate.name), str(user_certificate.candidate_id))
                    )
                else:
                    logging.getLogger('error_log').error(
                        "Error Occured for Certificate %s for Candidate Id %s" %
                        (str(certificate.name), str(user_certificate.candidate_id))
                    )
        if getattr(parsed_data.user_certificate, 'order_item_id'):
            if not user_certificates:
                logging.getLogger('error_log').error(
                    "Order Item id present , Certificate not available, badging not done" % (data)
                )
            orderitem_id = int(parsed_data.user_certificate.order_item_id)
            oi = OrderItem.objects.filter(id=orderitem_id).first()
            if certificate_updated:
                oi.orderitemoperation_set.create(
                    oi_status=191,
                    last_oi_status=oi.oi_status,
                    assigned_to=oi.assigned_to
                )
                subject = "Congrats, {} on completing the certification on {}".format(
                    oi.order.first_name, oi.product.name
                )
            last_oi_status = oi.oi_status
            oi.oi_status = 4
            oi.closed_on = timezone.now()
            oi.last_oi_status = 6
            oi.save()
            oi.orderitemoperation_set.create(
                oi_status=6,
                last_oi_status=last_oi_status,
                assigned_to=oi.assigned_to)
            oi.orderitemoperation_set.create(
                oi_status=oi.oi_status,
                last_oi_status=oi.last_oi_status,
                assigned_to=oi.assigned_to)
            to_emails = [oi.order.get_email()]
            mail_type = "CERTIFICATE_AND_ASSESMENT"
            data = {}
            data.update({
                "username": oi.order.first_name,
                "subject": subject,
                "product_name": oi.product.name,
                "skill_name": ', '.join(
                    list(ProductSkill.objects.filter(product=oi.product).values_list('skill__name', flat=True))
                ),
                "certificate_updated": certificate_updated,
                "score": parsed_data.assesment.overallScore,

            })
            create_assignment_lead.delay(obj_id=oi.id)
            send_email_task.delay(to_emails, mail_type, data, status=201, oi=oi.pk)
        else:
            logging.getLogger('error_log').error(
                "Order Item id not present , so unable close item related to this data ( %s ) " % (data)
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


class QuestionAnswerApiView(ListAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = QuestionAnswerSerializer
    pagination_class = None

    def get_queryset(self):
        id = self.request.GET.get('test_id')
        if not id:
            return Question.objects.none()
        return Question.objects.filter(test__id=id)

class VendorCertificateMappingApiView(ListAPIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorCertificateSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = super(self.__class__, self).get_queryset()
        name = self.request.GET.get('name', '')
        queryset = queryset.filter(slug=name)
        return queryset.exclude(certificate=None)

    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)

        return response


class ImportCertificateApiView(APIView, AmcatApiMixin):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]
    allowed_vendors = settings.IMPORT_CERTIFICATE_ALLOWED_VEDOR

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '')
        vendor_name = self.kwargs.get('vendor_name')
        if vendor_name not in self.allowed_vendors:
            return Response({
                "status": 1,
                "msg": "This vendor is not allowed for importing certificate"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not email:
            return Response({
                "status": 1,
                "msg": "Email is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        parser = CertiticateParser(parse_type=1)
        data = {
            'check_type': 'certificate',
            'candidate_email': email
        }
        success, data = self.get_all_certiticate_data(data)
        if success:
            if not data:
                data = {'certificates': []}
            logging.getLogger('info_log').error(
                "Certificate data for email %s is %s" % (str(email), str(data))
            )
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
        else:
            return Response(data, status=data['code'])


class TalentEconomyApiView(FieldFilterMixin, ListAPIView):
    """
    Include params -

    include_p_cat_id - Get data related to parent category
    include_p_user_id -Get data related to User


    Filter params-
    status -{ 0 for articles which are draft
             1 for articles which are published
             }

    visibility -{ 1 for ShineLearning
                 2 for TalentEconomy
                 3 for HR-Blogger
                 4 for HR-Conclave
                 5 for HR-Jobfair
                 }
    To view particular Fields only:
        include fl= id,title, (include fields with ',' separated)
    To view all articles do not include status and visibility in parameter

    To get the images for a particular size:
        Note:
            If you are using fl (include imagefield in it)
            Dimensions should be like 100 x 100

        For a particular size image
               add &image_fieldname_size=100x100
        For multiple size image
            add &image_fieldname_size=100x100,200x200,300x300


    pagination params-
            nopage -  get all results(unpaginated)
            page_size  - to get the how many result to be display per page

    Example:-

    {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 15,
                "title": "Questions To Ask During Job Interview - Learning.Shine"
            }
        ]
    }

    """
    permission_classes = []
    authentication_classes = []
    serializer_class = TalentEconomySerializer
    pagination_class = LearningCustomPagination

    def get_queryset(self, *args, **kwargs):
        status = self.request.GET.get('status', )
        visibility = self.request.GET.get('visibility')
        filter_dict = {}
        if status:
            filter_dict.update({'status': status})
        if visibility:
            filter_dict.update({'visibility': visibility})
        return Blog.objects.filter(**filter_dict)


class OrderDetailApiView(FieldFilterMixin, RetrieveAPIView):
    permission_classes = [IsAuthenticated, OrderAccessPermission]
    authentication_classes = [SessionAuthentication]
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        current_time = datetime.datetime.now().strftime("%d %B %Y %I:%M:%S %p")
        fields_to_check = self.get_required_fields()
        fields_to_log = ['email', 'alt_email', 'mobile', 'alt_mobile']
        for field in fields_to_log:
            if field not in fields_to_check:
                continue
            logging.getLogger('info_log').info('Order Data Accessed - {},{},{},{},{},{}'.format(current_time, \
                                                                                                user.id,
                                                                                                user.get_full_name(),
                                                                                                getattr(instance,
                                                                                                        'number',
                                                                                                        'None'), field,
                                                                                                getattr(instance, field,
                                                                                                        'None')))
        return self.retrieve(request, *args, **kwargs)


class OrderListApiView(FieldFilterMixin, ListAPIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OrderListSerializer
    pagination_class = LearningCustomPagination
    page_size = 1

    def get(self, request, *args, **kwargs):
        allowed_status = ['0', '1', '3']
        self.custom_status = self.request.query_params.get('status')
        if self.custom_status:
            self.custom_status = self.custom_status.split(',')
            allowed = all([i in allowed_status for i in self.custom_status])
            if not allowed:
                return Response(
                    {'message': 'Provide Valid Values for status'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            self.custom_status = [1, 3]
        self.custom_status = list(map(int, self.custom_status))
        return super(OrderListApiView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        vendor_ids = list(user.vendor_set.values_list('id', flat=True))
        items = OrderItem.objects.filter(
            product__vendor__id__in=vendor_ids,
            no_process=False,
            order__status__in= self.custom_status
        )
        return items


class CandidateInsight(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        logging.getLogger('info_log').info("Candidate Insight:- {}".format(str(data)))
        return Response({
            "msg": "Data has been noted."},
            status=status.HTTP_201_CREATED
        )

class TestTimer(APIView):
    permission_classes = []
    authentication_classes = []


    def get(self,request, *args, **kwargs):
        test_id = self.request.GET.get('test_id')
        duration = int(self.request.GET.get('duration',0))
        self.cache_test = TestCacheUtil(request=request)
        test_start_time = self.cache_test.get_start_test_cache(key='test-'+test_id)
        set_test_duration_cache = self.cache_test.get_test_duration_cache(key='test-'+test_id, duration=duration)
        #
        # if not timestamp:
        #     timestamp_with_tduration = (datetime.now() + timedelta(seconds=duration)).strftime(timeformat)
        #     test_ids = {'ongoing_' + str(test_id): timestamp_with_tduration}
        #     cache.set(test_session_key, test_ids, 60 * 60 * 24)
        #
        # elif timestamp and not timestamp.get('ongoing_' + str(test_id)):
        #     timestamp_with_tduration = (datetime.now() + timedelta(seconds=duration)).strftime(
        #         "%m/%d/%Y, %H:%M:%S")
        #     test_ids = {'ongoing_' + str(test_id): timestamp_with_tduration}
        #     cache.set(test_session_key, test_ids, 60 * 60 * 24)
        #
        # if not cache.get(session_id + 'startTest-' + str(test_id)):
        #     cache.set(session_id + 'startTest-' + str(test_id), datetime.now().strftime(timeformat),
        #               60 * 60 * 24)
        return Response({'testStartTime': test_start_time})


class SetSession(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self,request,*args,**kwargs):
        self.cache_test = TestCacheUtil(request=request)
        session_id = self.request.session.session_key
        data = {}
        key = None
        if not session_id:
            data.update({'is_set': False})
            return Response(data)
        timeout = self.request.POST.get('timeout','')
        submission = self.request.POST.get('submit','')
        test_id = self.request.POST.get('test_id','')
        lead_create = self.request.POST.get('lead_created','')
        key = 'test-' + str(test_id)
        # setting cache for timeout test sessions
        if timeout and test_id:
            self.cache_test.set_test_time_out(key)
            data.update({'is_set': True})

        # setting cache for submit test sessions

        if submission and test_id:
            key = 'test-' + test_id
            self.cache_test.set_test_submit(key)
            data.update({'is_set': True})

        # creating lead for particular session_id
        if lead_create:
            self.request._request.session.update({'is_lead_created': 1})
            return Response({'is_lead_created':True})

        return Response({'timeout': self.cache_test.get_test_time_out(key),
                         'submission': self.cache_test.get_test_submit(key)})

class RemoveCache(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self,request,*args,**kwargs):
        test_id = self.request.POST.get('test_id','')
        session_key = self.request.session.session_key
        key = session_key+'test-'+test_id
        cache_delete = cache.delete(key)
        return Response({'cache_delete': cache_delete})


class ServerTimeAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self,request,*args,**kwargs):
        self.time_format = "%m/%d/%Y, %H:%M:%S"
        if self.request.GET.get('time_format'):
            return Response({'time':datetime.datetime.now().strftime(self.request.GET.get('time_format'))})
        if self.request.GET.get('time_stamp'):
            return Response({'time': datetime.datetime.timestamp(datetime.datetime.now())})
        return Response({'time':datetime.datetime.now().strftime(self.time_format)})


class ClaimOrderAPIView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self,request):
        txn_id = self.request.POST.get('txn_id',None)
        email = self.request.POST.get('email',None)
        alt_email = self.request.POST.get('alt_email',None)
        mobile = self.request.POST.get('mobile',"")[-10:]
        alt_mobile = self.request.POST.get('alt_mobile',"")[-10:]
        user_id = self.request.POST.get('user_id',None)
        lead_id = self.request.POST.get('lead_id',None)
        name = self.request.POST.get('name', None)

        sales_user_info = self.request.POST.get('sales_user_info')
        data = {'claim_order': False}
        if not txn_id:
            data.update({'msg': "Transaction id not found"})
            return Response(data, status=400)
        payment_object = PaymentTxn.objects.filter(txn=txn_id,status=1).first()
        if not payment_object:
            data.update({'msg': "Transaction object not found "})
            return Response(data, status=400)
        order = payment_object.order
        if not order:
            data.update({'msg': "Order object not found "})
            return Response(data,  status=400)
        if (email and getattr(order, 'email') == email) or\
                (mobile and getattr(order, 'mobile') == mobile) or\
                 (name and order.full_name == name):
            if order.sales_user_info or order.crm_lead_id or order.crm_sales_id:
                data.update({'msg': "Order is already claimed"})
                return Response(data, status=400)
            if not user_id or not lead_id or not sales_user_info:
                return Response(data, status=400)
            order.crm_lead_id = lead_id
            order.crm_sales_id = user_id
            order.sales_user_info = sales_user_info
            order.save()
            data.update({'claim_order': True,'msg': 'Order claimed '
                         'successfully','order_amount':order.total_incl_tax})
            return Response(data)
        data.update({"msg": "Invalid details"})
        return Response(data, status=400)



class GetAutoLoginToken(APIView):
     authentication_classes = [SessionAuthentication]
     permission_classes = [IsAuthenticated]

     def get(self,request,*args,**kwargs):

         order_item_id = kwargs.get('order_item_id','')
         order_item = OrderItem.objects.filter(id=order_item_id).first()
         if not order_item:
             return Response({"token":'', "msg": 'Invalid Order Item Id'}, status=status.HTTP_400_BAD_REQUEST)

         email  = order_item.order.email;
         candidate_id = order_item.order.candidate_id;
         token_gen = AutoLogin()
         login_token = token_gen.encode(email, candidate_id, None)
         return Response({"token": login_token, "msg": "Successfull"}, status=status.HTTP_200_OK)

class GetCacheValue(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        key = request.GET.get('key','')
        if not key: 
            return Response({
                'value':''
            }, status=status.HTTP_400_BAD_REQUEST)
        value = cache.get(key,'')
        return Response({
            'value': value
        }, status=status.HTTP_200_OK)



        






















