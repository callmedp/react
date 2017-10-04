import logging

from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser, )
from oauth2_provider.contrib.rest_framework import OAuth2Authentication

from users.tasks import user_register
from order.models import Order
from shop.views import ProductInformationMixin
from shop.models import Product
from order.functions import update_initiat_orderitem_sataus


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
                    order.first_name = name
                    order.currency = int(request.data.get('currency', 0))
                    order.tax_config = ''
                    order.status = 1
                    order.total_excl_tax = request.data.get('total_excl_tax_excl_discount', 0)
                    order.total_incl_tax = request.data.get('total_payable_amount', 0)
                    order.save()

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
                                oi.upc = str(order.pk) + "_" + str(oi.pk)
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

                        for var in variations:
                            prd = Product.objects.get(id=var.get('id'))
                            oi = order.orderitems.create(
                                product=prd,
                                title=prd.get_name,
                                partner=prd.vendor,
                                parent=p_oi,
                                is_variation=True,
                            )
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