import logging

from django.utils import timezone

from cart.mixins import CartMixin
from shop.views import ProductInformationMixin
from linkedin.models import Draft, Organization, Education
from quizs.models import QuizResponse
from users.tasks import user_register

from .models import Order, OrderItem
from .functions import update_initiat_orderitem_sataus


class OrderMixin(CartMixin, ProductInformationMixin):

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
                order = Order.objects.create(cart=cart_obj, date_placed=timezone.now())
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
                order.currency = 'Rs.'

                order.total_excl_tax = self.getTotalAmount(cart_obj=cart_obj)
                order.save()


                if order.status == 2 and (order.payment_mode == 1 or order.payment_mode == 4):
                    to_emails = [order.email]
                    mail_type = "PAYMENT_PENDING"
                    data = {}
                    data.update({
                        "subject": 'Your shine payment confirmation',
                        "first_name": order.first_name if order.first_name else order.candidate_id,
                        "transactionid": order.txn,
                    })
                    try:
                        SendMail().send(to_emails, mail_type, login_dict)
                    except Exception as e:
                        logging.getLogger('email_log').error("%s - %s - %s" % (str(to_emails), str(mail_type), str(e)))
                        pass

                self.createOrderitems(order, cart_obj)
                # update initial operation status
                update_initiat_orderitem_sataus(order=order)

                if not order.candidate_id:
                    user_register(data={}, order=order.pk)

                # for linkedin
                order_items = order.orderitems.filter(product__type_flow__in=[8])

                if order.orderitems.filter(product__type_flow__in=[1, 3, 4, 5, 12,13]) and order.status == 1:
                    to_emails = [order.email]
                    mail_type = "MIDOUT"
                    data = {}
                    data.update({
                        "subject": 'To initiate your services fulfil these details',
                        "username": order.first_name if order.first_name else order.candidate_id,
                        "flag": 'uploadresume',
                    })
                    try:
                        SendMail().send(to_emails, mail_type, data)
                        order.midout_sent_on = timezone.now()
                    except Exception as e:
                        logging.getLogger('email_log').error("reminder cron %s - %s - %s" % (str(to_emails), str(mail_type), str(e)))

                    try:
                        SendSMS().send(sms_type=mail_type, data=data)
                    except Exception as e:
                        logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                if order_items:
                    # associate draft object with order
                    order_item = order_items.first()
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
                            oi.oi_price_before_discounts_excl_tax = product.get_price()
                            oi.save()

                        addons = item.get('addons')
                        for addon in addons:
                            oi = OrderItem.objects.create(
                                order=order,
                                product=addon.product,
                                title=addon.product.name,
                                partner=addon.product.vendor
                            )
                            oi.upc = str(order.pk) + "_" + str(oi.pk)
                            oi.parent = p_oi
                            oi.oi_price_before_discounts_excl_tax = addon.price_excl_tax
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
                        p_oi.oi_price_before_discounts_excl_tax = parent_li.price_excl_tax
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
                            oi.oi_price_before_discounts_excl_tax = var.price_excl_tax
                            oi.is_variation = True
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
                            oi.oi_price_before_discounts_excl_tax = addon.price_excl_tax
                            oi.save()

        except Exception as e:
            logging.getLogger('error_log').error(str(e))
