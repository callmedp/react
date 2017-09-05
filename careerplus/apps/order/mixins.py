import logging
import json
import datetime

from decimal import Decimal

from django.utils import timezone

from cart.mixins import CartMixin
from shop.views import ProductInformationMixin
from linkedin.models import Draft, Organization, Education
from quizs.models import QuizResponse
from users.tasks import user_register
from wallet.models import Wallet

from .models import Order, OrderItem
from .functions import (
    update_initiat_orderitem_sataus,)


class OrderMixin(CartMixin, ProductInformationMixin):

    def addRewardPointInWallet(self, order=None):
        if order and order.candidate_id and order.status == 1:
            wal_obj, created = Wallet.objects.get_or_create(
                owner=order.candidate_id)
            # reward point 10% of payable amount
            reward_point = (order.total_incl_tax * 10) / 100
            reward_point = round(reward_point, 0)

            expiry = timezone.now() + datetime.timedelta(days=30)
            wal_obj.point.create(
                original=reward_point,
                current=reward_point,
                expiry=expiry,
                status=1,
                txn=order.number
            )

    def fridge_cart(self, cart_obj):
        if cart_obj:
            cart_obj.date_submitted = timezone.now()
            cart_obj.is_submitted = True
            cart_obj.date_frozen = timezone.now()
            cart_obj.last_status = cart_obj.status
            cart_obj.status = 4
            cart_obj.save()
            return cart_obj

    def get_cart_last_status(self, cart_obj):
        cart_status = cart_obj.status
        cart_obj.status = cart_obj.last_status
        cart_obj.last_status = cart_status
        cart_obj.save()
        return cart_obj

    def createOrder(self, cart_obj):
        try:
            candidate_id = self.request.session.get('candidate_id')
            if cart_obj:
                order = Order.objects.create(date_placed=timezone.now())
                order.number = 'CP' + str(order.pk)
                if candidate_id:
                    order.candidate_id = candidate_id

                order.email = cart_obj.email
                order.first_name = cart_obj.first_name
                order.last_name = cart_obj.last_name
                order.country_code = cart_obj.country_code
                order.mobile = cart_obj.mobile
                order.address = cart_obj.address
                order.pincode = cart_obj.pincode
                order.state = cart_obj.state
                order.country = cart_obj.country

                # set currency
                order.currency = 'INR'

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
                order.total_excl_tax = total_amount  # before discount amount
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

                self.createOrderitems(order, cart_obj)

                # update initial operation status
                update_initiat_orderitem_sataus(order=order)

                # add reward_point in wallet
                self.addRewardPointInWallet(order=order)

                if not order.candidate_id:
                    user_register(data={}, order=order.pk)

                # for linkedin
                linkedin_product = order.orderitems.filter(product__type_flow=8)

                if linkedin_product:
                    # associate draft object with order
                    order_item = linkedin_product.first()
                    draft_obj = Draft.objects.create()
                    org_obj = Organization()
                    org_obj.draft = draft_obj
                    org_obj.save()

                    edu_obj = Education()
                    edu_obj.draft = draft_obj
                    edu_obj.save()

                    quiz_rsp = QuizResponse()
                    quiz_rsp.oi = order_item
                    quiz_rsp.save()

                    order_item.counselling_form_status = 41
                    order_item.oio_linkedin = draft_obj
                    order_item.save()
                return order
        except Exception as e:
            logging.getLogger('error_log').error(str(e))

    def createOrderitems(self, order, cart_obj):
        try:
            if order and cart_obj:
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

                percentage_discount = (total_discount * 100) / total_amount_before_discount

                self.request.session.update({
                    "order_pk": order.pk,
                })
                cart_items = self.get_cart_items()
                for item in cart_items:
                    parent_li = item.get('li')

                    if parent_li and parent_li.product.type_product == 3:
                        p_oi = OrderItem.objects.create(
                            order=order,
                            product=parent_li.product,
                            title=parent_li.product.name,
                            partner=parent_li.product.vendor,
                            is_combo=True,
                            no_process=True,
                        )
                        p_oi.upc = str(order.pk) + "_" + str(p_oi.pk)
                        p_oi.oi_price_before_discounts_excl_tax = parent_li.product.get_price()
                        price_incl_tax = parent_li.product.get_price() + ((parent_li.product.get_price() * tax_rate_per) / 100)
                        p_oi.oi_price_before_discounts_incl_tax = price_incl_tax

                        cost_price = parent_li.product.get_price()
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
                            # oi.oi_price_before_discounts_excl_tax = product.get_price()
                            # price_incl_tax = product.get_price() + ((product.get_price() * tax_rate_per) / 100)
                            # oi.oi_price_before_discounts_incl_tax = price_incl_tax
                            if parent_li.delivery_service:
                                oi.delivery_service = parent_li.delivery_service
                            oi.save()

                        addons = item.get('addons')
                        for addon in addons:
                            oi = OrderItem.objects.create(
                                order=order,
                                product=addon.product,
                                title=addon.product.name,
                                partner=addon.product.vendor,
                                is_addon=True,
                            )
                            oi.upc = str(order.pk) + "_" + str(oi.pk)
                            oi.parent = p_oi
                            oi.oi_price_before_discounts_excl_tax = addon.product.get_price()
                            price_incl_tax = addon.product.get_price() + ((addon.product.get_price() * tax_rate_per) / 100)
                            oi.oi_price_before_discounts_incl_tax = price_incl_tax
                            if parent_li.delivery_service:
                                oi.delivery_service = parent_li.delivery_service
                            oi.save()

                    elif parent_li:
                        p_oi = OrderItem.objects.create(
                            order=order,
                            product=parent_li.product,
                            title=parent_li.product.name,
                            partner=parent_li.product.vendor,
                            no_process=parent_li.no_process,
                        )
                        p_oi.upc = str(order.pk) + "_" + str(p_oi.pk)

                        p_oi.oi_price_before_discounts_excl_tax = parent_li.product.get_price()
                        price_incl_tax = parent_li.product.get_price() + ((parent_li.product.get_price() * tax_rate_per) / 100)
                        p_oi.oi_price_before_discounts_incl_tax = price_incl_tax
                        if parent_li.delivery_service:
                            p_oi.delivery_service = parent_li.delivery_service
                            p_oi.delivery_price_excl_tax = parent_li.delivery_service.get_price()
                            price_incl_tax = parent_li.delivery_service.get_price() + ((parent_li.delivery_service.get_price() * tax_rate_per) / 100)
                            p_oi.delivery_price_incl_tax = price_incl_tax
                        p_oi.save()

                        variations = item.get('variations')
                        for var in variations:
                            oi = OrderItem.objects.create(
                                order=order,
                                product=var.product,
                                title=var.product.name,
                                partner=var.product.vendor
                            )
                            oi.upc = str(order.pk) + "_" + str(oi.pk)
                            oi.parent = p_oi
                            oi.oi_price_before_discounts_excl_tax = var.product.get_price()
                            price_incl_tax = var.product.get_price() + ((var.product.get_price() * tax_rate_per) / 100)
                            oi.oi_price_before_discounts_incl_tax = price_incl_tax
                            oi.is_variation = True
                            if parent_li.delivery_service:
                                # in case other variation in which base price included
                                oi.delivery_service = parent_li.delivery_service
                            elif var.delivery_service:
                                # in case of course variation
                                oi.delivery_service = var.delivery_service
                                oi.delivery_price_excl_tax = var.delivery_service.get_price()
                                price_incl_tax = var.delivery_service.get_price() + ((var.delivery_service.get_price() * tax_rate_per) / 100)
                                oi.delivery_price_incl_tax = var.delivery_service.get_price()
                            oi.save()

                        addons = item.get('addons')
                        for addon in addons:
                            oi = OrderItem.objects.create(
                                order=order,
                                product=addon.product,
                                title=addon.product.name,
                                partner=addon.product.vendor,
                                is_addon=True,
                            )
                            oi.upc = str(order.pk) + "_" + str(oi.pk)
                            oi.parent = p_oi
                            oi.oi_price_before_discounts_excl_tax = addon.product.get_price()
                            price_incl_tax = addon.product.get_price() + ((addon.product.get_price() * tax_rate_per) / 100)
                            oi.oi_price_before_discounts_incl_tax = price_incl_tax
                            if parent_li.delivery_service:
                                oi.delivery_service = parent_li.delivery_service
                            oi.save()

        except Exception as e:
            logging.getLogger('error_log').error(str(e))



