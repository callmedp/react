import json
import datetime

from decimal import Decimal

from django.utils import timezone

from cart.mixins import CartMixin
from shop.views import ProductInformationMixin
from linkedin.models import Draft, Organization, Education
from quizs.models import QuizResponse
from wallet.models import Wallet
from order.tasks import service_initiation

from .models import Order, OrderItem
from .functions import (
    update_initiat_orderitem_sataus, )


class OrderMixin(CartMixin, ProductInformationMixin):

    def addRewardPointInWallet(self, order=None):
        if order and order.candidate_id and order.status == 1:
            wal_obj, created = Wallet.objects.get_or_create(
                owner=order.candidate_id)
            wal_obj.owner_email = order.email
            wal_obj.save()
            # reward point 10% of payable amount
            reward_point = (order.total_incl_tax * 10) / 100
            reward_point = round(reward_point, 0)

            expiry = timezone.now() + datetime.timedelta(days=30)

            point_obj = wal_obj.point.create(
                original=reward_point,
                current=reward_point,
                expiry=expiry,
                status=1,
                txn=order.number
            )

            wal_txn = wal_obj.wallettxn.create(
                txn_type=1,
                status=1,
                order=order,
                txn=order.number,
                point_value=reward_point
            )

            point_obj.wallettxn.create(
                transaction=wal_txn,
                point_value=reward_point,
                txn_type=1
            )

            current_value = wal_obj.get_current_amount()
            wal_txn.current_value = current_value
            wal_txn.save()

    def createOrder(self, cart_obj):
        candidate_id = self.request.session.get('candidate_id')
        if cart_obj and cart_obj.status not in [1, 5, 6]:
            order = Order.objects.create(date_placed=timezone.now())
            order.number = 'CP' + str(order.pk)
            if candidate_id:
                order.candidate_id = candidate_id
            else:
                order.candidate_id = cart_obj.owner_id

            order.email = cart_obj.email
            order.alt_email = cart_obj.email
            order.first_name = cart_obj.first_name
            order.last_name = cart_obj.last_name
            order.country_code = cart_obj.country_code
            order.mobile = cart_obj.mobile
            order.alt_mobile = cart_obj.mobile
            order.address = cart_obj.address
            order.pincode = cart_obj.pincode
            order.state = cart_obj.state
            order.country = cart_obj.country
            order.utm_params = json.loads(self.request.session.get('utm',{}))

            # set currency
            order.currency = 0

            payment_dict = self.getPayableAmount(cart_obj=cart_obj)
            total_amount = payment_dict.get('total_amount')
            total_payable_amount = payment_dict.get('total_payable_amount')
            tax_dict = {}
            tax_dict.update({
                "sgst": payment_dict.get('sgst'),
                "cgst": payment_dict.get('cgst'),
                "igst": payment_dict.get('igst')})
            tax_dict = json.dumps(tax_dict)
            order.tax_config = tax_dict
            order.total_excl_tax = total_amount  # before discount amount and before tax
            if total_payable_amount <= 0:
                total_payable_amount = Decimal(0)
            order.total_incl_tax = total_payable_amount  # payable amount including tax and excluding discount
            order.save()

            # coupon applied or loyalty point handling
            wal_txn = cart_obj.wallettxn.filter(txn_type=2).order_by('-created').select_related('wallet')

            if cart_obj.coupon:
                coupon_amount = payment_dict.get('coupon_amount')
                order.couponorder_set.create(
                    coupon=cart_obj.coupon,
                    coupon_code=cart_obj.coupon.code,
                    value=coupon_amount,
                )
            elif wal_txn.exists():
                wal_txn = wal_txn[0]
                wal_txn.order = order
                wal_txn.save()

            self.createOrderitems(order, cart_obj, payment_dict)

            # update initial operation status
            update_initiat_orderitem_sataus(order=order)
            service_initiation.delay(order.pk)
            # for linkedin
            linkedin_products = order.orderitems.filter(product__type_flow=8)

            for linkedin_product in linkedin_products:
                # associate draft object with order
                order_item = linkedin_product
                last_oi_status = order_item.oi_status
                draft_obj = Draft.objects.create()
                org_obj = Organization()
                org_obj.draft = draft_obj
                org_obj.save()

                edu_obj = Education()
                edu_obj.draft = draft_obj
                edu_obj.save()

                quiz_rsp = QuizResponse()
                quiz_rsp.oi = linkedin_product
                quiz_rsp.save()

                order_item.oi_status = 2
                order_item.last_oi_status = last_oi_status
                order_item.oio_linkedin = draft_obj
                order_item.save()
                order_item.orderitemoperation_set.create(
                    oi_status=order_item.oi_status,
                    last_oi_status=last_oi_status,
                )
            return order

    def createOrderitems(self, order, cart_obj, payment_dict={}):
        if order and cart_obj:
            if not payment_dict:
                payment_dict = self.getPayableAmount(cart_obj=cart_obj)
            tax_rate_per = payment_dict.get('tax_rate_per')
            total_amount_before_discount = payment_dict.get('total_amount')

            coupon_amount = Decimal(0)
            coupons_applied = order.couponorder_set.all()
            for coupon in coupons_applied:
                coupon_amount += coupon.value

            # loyalty point used
            redeemed_reward_point = Decimal(0)
            wal_txn = order.wallettxn.filter(txn_type=2).order_by('-created').select_related('wallet')
            if wal_txn.exists():
                wal_txn = wal_txn[0]
                redeemed_reward_point = wal_txn.point_value

            total_discount = coupon_amount + redeemed_reward_point

            if total_amount_before_discount:
                percentage_discount = (total_discount * 100) / total_amount_before_discount
            else:
                percentage_discount = 0

            self.request.session.update({
                "order_pk": order.pk,
            })

            # cart_dict = self.get_solr_cart_items(cart_obj=cart_obj)
            line_item = cart_obj.lineitems.filter(parent=None)[0]
            type_flow = int(line_item.product.type_flow)

            # resume builder flow handle
            if type_flow == 17:
                cart_dict = self.get_local_cart_items(cart_obj=cart_obj)
            else:
                cart_dict = self.get_solr_cart_items(cart_obj=cart_obj)

            cart_items = cart_dict.get('cart_items', [])
            for item in cart_items:
                if item.get('is_available'):

                    parent_li = item.get('li')

                    if parent_li and parent_li.product.type_product == 3:
                        p_oi = OrderItem.objects.create(
                            order=order,
                            product=parent_li.product,
                            title=item.get('name'),
                            partner=parent_li.product.vendor,
                            is_combo=True,
                            no_process=True,
                        )
                        p_oi.upc = str(order.pk) + "_" + str(p_oi.pk)
                        # p_oi.oi_price_before_discounts_excl_tax = item.get('price')
                        # price_incl_tax = item.get('price') + ((item.get('price') * tax_rate_per) / 100)
                        # p_oi.oi_price_before_discounts_incl_tax = price_incl_tax

                        cost_price = item.get('price')
                        p_oi.cost_price = cost_price
                        discount = (cost_price * percentage_discount) / 100
                        cost_price_after_discount = cost_price - discount
                        tax_amount = (cost_price_after_discount * tax_rate_per) / 100
                        selling_price = cost_price_after_discount + tax_amount
                        p_oi.selling_price = selling_price
                        p_oi.tax_amount = tax_amount
                        p_oi.discount_amount = discount

                        if parent_li.delivery_service:
                            p_oi.delivery_service = parent_li.delivery_service
                            cost_price = parent_li.delivery_service.get_price()
                            p_oi.delivery_price_excl_tax = cost_price
                            discount = (cost_price * percentage_discount) / 100
                            cost_price_after_discount = cost_price - discount
                            tax_amount = (cost_price_after_discount * tax_rate_per) / 100
                            selling_price = cost_price_after_discount + tax_amount
                            p_oi.delivery_price_incl_tax = selling_price
                        p_oi.save()

                        combos = self.get_combos(parent_li.product).get('combos')

                        for product in combos:
                            oi = OrderItem.objects.create(
                                order=order,
                                product=product,
                                title=product.pv_name(),
                                partner=product.vendor
                            )
                            oi.upc = str(order.pk) + "_" + str(oi.pk)
                            oi.parent = p_oi
                            oi.is_combo = True
                            cost_price = product.get_price()
                            oi.cost_price = cost_price
                            oi.selling_price = 0
                            oi.tax_amount = 0
                            oi.discount_amount = 0

                            if parent_li.delivery_service:
                                oi.delivery_service = parent_li.delivery_service
                            oi.save()

                        addons = item.get('addons')
                        for addon in addons:
                            if addon.get('is_available'):
                                child_li = addon.get('li')
                                oi = OrderItem.objects.create(
                                    order=order,
                                    product=child_li.product,
                                    title=addon.get('name'),
                                    partner=child_li.product.vendor,
                                    is_addon=True,
                                )
                                oi.upc = str(order.pk) + "_" + str(oi.pk)
                                oi.parent = p_oi
                                # oi.oi_price_before_discounts_excl_tax = addon.get('price')
                                # price_incl_tax = addon.get('price') + ((addon.get('price') * tax_rate_per) / 100)
                                # oi.oi_price_before_discounts_incl_tax = price_incl_tax

                                cost_price = addon.get('price')
                                oi.cost_price = cost_price
                                discount = (cost_price * percentage_discount) / 100
                                cost_price_after_discount = cost_price - discount
                                tax_amount = (cost_price_after_discount * tax_rate_per) / 100
                                selling_price = cost_price_after_discount + tax_amount
                                oi.selling_price = selling_price
                                oi.tax_amount = tax_amount
                                oi.discount_amount = discount

                                if parent_li.delivery_service:
                                    oi.delivery_service = parent_li.delivery_service
                                oi.save()

                    elif parent_li:
                        p_oi = OrderItem.objects.create(
                            order=order,
                            product=parent_li.product,
                            title=item.get('name'),
                            partner=parent_li.product.vendor,
                            no_process=parent_li.no_process,
                        )
                        p_oi.upc = str(order.pk) + "_" + str(p_oi.pk)

                        # p_oi.oi_price_before_discounts_excl_tax = item.get('price')
                        # price_incl_tax = item.get('price') + ((item.get('price') * tax_rate_per) / 100)
                        # p_oi.oi_price_before_discounts_incl_tax = price_incl_tax

                        cost_price = item.get('price')
                        p_oi.cost_price = cost_price
                        discount = (cost_price * percentage_discount) / 100
                        cost_price_after_discount = cost_price - discount
                        tax_amount = (cost_price_after_discount * tax_rate_per) / 100
                        selling_price = cost_price_after_discount + tax_amount
                        p_oi.selling_price = selling_price
                        p_oi.tax_amount = tax_amount
                        p_oi.discount_amount = discount

                        if parent_li.delivery_service:
                            p_oi.delivery_service = parent_li.delivery_service

                            cost_price = parent_li.delivery_service.get_price()
                            p_oi.delivery_price_excl_tax = cost_price
                            discount = (cost_price * percentage_discount) / 100
                            cost_price_after_discount = cost_price - discount
                            tax_amount = (cost_price_after_discount * tax_rate_per) / 100
                            selling_price = cost_price_after_discount + tax_amount
                            p_oi.delivery_price_incl_tax = selling_price

                        variations = item.get('variations')
                        if variations:
                            p_oi.is_variation = True
                            if item.get('product_class', '') == 'course':
                                p_oi.selling_price = 0
                                p_oi.tax_amount = 0
                                p_oi.discount_amount = 0

                        p_oi.save()

                        for var in variations:
                            if var.get('is_available'):

                                child_li = var.get('li')
                                oi = OrderItem.objects.create(
                                    order=order,
                                    product=child_li.product,
                                    title=var.get('name'),
                                    partner=child_li.product.vendor
                                )
                                oi.upc = str(order.pk) + "_" + str(oi.pk)
                                oi.parent = p_oi
                                # oi.oi_price_before_discounts_excl_tax = var.get('price')
                                # price_incl_tax = var.get('price') + ((var.get('price') * tax_rate_per) / 100)
                                # oi.oi_price_before_discounts_incl_tax = price_incl_tax

                                cost_price = var.get('price')
                                oi.cost_price = cost_price
                                discount = (cost_price * percentage_discount) / 100
                                cost_price_after_discount = cost_price - discount
                                tax_amount = (cost_price_after_discount * tax_rate_per) / 100
                                selling_price = cost_price_after_discount + tax_amount
                                oi.selling_price = selling_price
                                oi.tax_amount = tax_amount
                                oi.discount_amount = discount

                                oi.is_variation = True
                                if parent_li.delivery_service:
                                    # in case other variation in which base price included
                                    oi.delivery_service = parent_li.delivery_service
                                elif child_li.delivery_service:
                                    # in case of course variation
                                    delivery_obj = var.get('delivery_obj')
                                    oi.delivery_service = delivery_obj
                                    cost_price = delivery_obj.get_price()
                                    oi.delivery_price_excl_tax = cost_price
                                    discount = (cost_price * percentage_discount) / 100
                                    cost_price_after_discount = cost_price - discount
                                    tax_amount = (cost_price_after_discount * tax_rate_per) / 100
                                    selling_price = cost_price_after_discount + tax_amount
                                    oi.delivery_price_incl_tax = selling_price
                                oi.save()

                        addons = item.get('addons')
                        for addon in addons:
                            if addon.get('is_available'):
                                child_li = addon.get('li')
                                oi = OrderItem.objects.create(
                                    order=order,
                                    product=child_li.product,
                                    title=addon.get('name'),
                                    partner=child_li.product.vendor,
                                    is_addon=True,
                                )
                                oi.upc = str(order.pk) + "_" + str(oi.pk)
                                oi.parent = p_oi
                                # oi.oi_price_before_discounts_excl_tax = addon.get('price')
                                # price_incl_tax = addon.get('price') + ((addon.get('price') * tax_rate_per) / 100)
                                # oi.oi_price_before_discounts_incl_tax = price_incl_tax

                                cost_price = addon.get('price')
                                oi.cost_price = cost_price
                                discount = (cost_price * percentage_discount) / 100
                                cost_price_after_discount = cost_price - discount
                                tax_amount = (cost_price_after_discount * tax_rate_per) / 100
                                selling_price = cost_price_after_discount + tax_amount
                                oi.selling_price = selling_price
                                oi.tax_amount = tax_amount
                                oi.discount_amount = discount

                                if parent_li.delivery_service:
                                    oi.delivery_service = parent_li.delivery_service
                                oi.save()
