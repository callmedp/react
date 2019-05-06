import logging
import json
import operator

from decimal import Decimal

from django.utils import timezone
from django.conf import settings

from haystack.query import SearchQuerySet

from shop.models import Product, ProductClass
from partner.models import Vendor
from core.mixins import InvoiceGenerate
from geolocation.models import Country

from .models import Cart, LineItem

from django.db.models import Q


class CartMixin(object):
    def mergeCart(self, fromcart, tocart):
        try:
            from_parent_lines = fromcart.lineitems.filter(parent=None).select_related('product')
            to_parent_pks = tocart.lineitems.filter(parent=None).values_list('product__pk', flat=True)

            for main_p in from_parent_lines:
                if main_p.product.pk in to_parent_pks:
                    parent_product = tocart.lineitems.get(product=main_p.product)
                    to_child_pks = tocart.lineitems.filter(parent=parent_product).values_list('product__pk', flat=True)
                    from_child_lines = fromcart.lineitems.filter(parent=main_p).select_related('product')

                    for child in from_child_lines:
                        if child.product.pk not in to_child_pks:
                            li = tocart.lineitems.create(product=child.product)
                            li.reference = str(tocart.pk) + '_' + str(li.pk)
                            li.price_excl_tax = child.product.get_price()
                            li.save()

                else:
                    parent_product = tocart.lineitems.create(product=main_p.product)
                    parent_product.reference = str(tocart.pk) + '_' + str(parent_product.pk)
                    parent_product.price_excl_tax = main_p.product.get_price()
                    parent_product.save()
                    from_child_lines = fromcart.lineitems.filter(parent=main_p).select_related('product')

                    for child in from_child_lines:
                        li = tocart.lineitems.create(parent=parent_product, product=child.product)
                        li.reference = str(tocart.pk) + '_' + str(li.pk)
                        li.price_excl_tax = child.product.get_price()
                        li.save()
                main_p.delete()

            fromcart.status = 1
            fromcart.date_merged = timezone.now()
            fromcart.save()
        except Exception as e:
            logging.getLogger('error_log').error(str(e))

    def updateCart(self, product: object, addons: object, cv_id: object, add_type: object,
                   req_options: object, is_resume_template) -> object:
        flag = -1
        try:
            flag = 1
            candidate_id = self.request.session.get('candidate_id')
            email = self.request.session.get('email')
            mobile = self.request.session.get('mobile_no')
            country_code = self.request.session.get('country_code')
            if add_type == "cart":
                self.getCartObject()
                cart_pk = self.request.session.get('cart_pk')
                session_id = self.request.session.session_key

                if cart_pk:
                    cart_obj = Cart.objects.get(pk=cart_pk)
                elif candidate_id:
                    cart_obj = Cart.objects.create(owner_id=candidate_id, session_id=session_id, status=2)
                elif session_id:
                    cart_obj = Cart.objects.create(session_id=session_id, status=0)
            elif add_type == "express":
                if not self.request.session.session_key:
                    self.request.session.create()
                session_id = self.request.session.session_key
                if candidate_id:
                    cart_obj = Cart.objects.create(owner_id=candidate_id, session_id=session_id, status=3)
                elif session_id:
                    cart_obj = Cart.objects.create(session_id=session_id, status=3)

            if cart_obj:
                if email and not cart_obj.owner_email:
                    cart_obj.owner_email = email
                    if not cart_obj.email:
                        cart_obj.email = email
                    cart_obj.save()

                if country_code and not cart_obj.country_code:
                    try:
                        country_obj = Country.objects.get(phone=country_code, active=True)
                    except Exception as e:
                        logging.getLogger('error_log').error('unable to get country object%s' % str(e))
                        country_obj = Country.objects.get(phone='91', active=True)

                    cart_obj.country_code = country_obj.phone
                    cart_obj.save()

                if mobile and not cart_obj.mobile:
                    cart_obj.mobile = mobile
                    cart_obj.save()

                # todo update it for resume builder only
                if is_resume_template == 'true':
                    cart_obj.lineitems.filter().delete()
                else:
                    cart_obj.lineitems.filter(Q(product=product) | Q(product__type_flow=16)).delete()

                if product.is_course or product.type_flow == 16 and cv_id:
                    # courses
                    try:
                        # for resume builder type_flow todo create new type flow
                        if product.type_flow == 16:
                            cv_prod = Product.objects.get(id=cv_id)
                        else:
                            cv_prod = Product.objects.get(id=cv_id, active=True)
                        parent = cart_obj.lineitems.create(product=product, no_process=True)
                        parent.reference = str(cart_obj.pk) + '_' + str(parent.pk)
                        parent.price_excl_tax = product.get_price()
                        parent.save()
                        child = cart_obj.lineitems.create(product=cv_prod, parent=parent)
                        child.reference = str(cart_obj.pk) + '_' + str(child.pk)
                        child.price_excl_tax = cv_prod.get_price()
                        child.parent_deleted = True
                        child.save()

                        # for addons
                        child_products = product.related.filter(
                            secondaryproduct__active=True)
                        addons = Product.objects.filter(id__in=addons)
                        for child in addons:
                            if child in child_products:
                                li = LineItem.objects.create(cart=cart_obj, parent=parent, product=child)
                                li.reference = str(cart_obj.pk) + '_' + str(li.pk)
                                li.price_excl_tax = child.get_price()
                                li.save()
                    except Exception as e:
                        logging.getLogger('error_log').error(str(e))
                else:
                    # standalone/Combo/coutry-specific
                    parent = LineItem.objects.create(cart=cart_obj, product=product)
                    parent.reference = str(cart_obj.pk) + '_' + str(parent.pk)
                    parent.price_excl_tax = product.get_price()
                    parent.save()
                    child_products = product.related.filter(
                        secondaryproduct__active=True)
                    addons = Product.objects.filter(id__in=addons)
                    for child in addons:
                        if child in child_products:
                            li = LineItem.objects.create(cart=cart_obj, parent=parent, product=child)
                            li.reference = str(cart_obj.pk) + '_' + str(li.pk)
                            li.price_excl_tax = child.get_price()
                            li.save()

                    req_products = Product.objects.filter(id__in=req_options)
                    if req_products.exists():
                        parent.no_process = True
                        parent.save()
                        for prd in req_products:
                            li = LineItem.objects.create(cart=cart_obj, parent=parent, product=prd)
                            li.reference = str(cart_obj.pk) + '_' + str(li.pk)
                            li.price_excl_tax = prd.get_price()
                            li.parent_deleted = True
                            li.save()

                self.request.session.update({
                    "cart_pk": cart_obj.pk,
                    "checkout_type": add_type,
                })

                if add_type == "cart":
                    self.request.session.update({
                        "cart_count_pk": cart_obj.pk,
                    })

            return flag

        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return flag

    def getCartObject(self, request: object = None) -> object:
        try:
            cart_obj = None
            if not request:
                request = self.request
            candidate_id = request.session.get('candidate_id')
            if not request.session.session_key:
                request.session.create()
            sessionid = request.session.session_key
            cart_users = []
            if candidate_id:
                cart_users = Cart.objects.filter(owner_id=candidate_id, status=2)

            cart_sessions = Cart.objects.filter(session_id=sessionid, status=0)
            cart_user, cart_session = None, None
            if cart_users:
                for cart in cart_users:
                    if cart_user:
                        self.mergeCart(cart, cart_user)
                    else:
                        cart_user = cart
                # cart_user = cart_users[0]
            if cart_sessions:
                for cart in cart_sessions:
                    if cart_session:
                        self.mergeCart(cart, cart_session)
                    else:
                        cart_session = cart
                # cart_session = cart_sessions[0]

            if cart_user and cart_session and (cart_user != cart_session):
                self.mergeCart(cart_session, cart_user)

            if cart_user:
                cart_obj = cart_user
            elif cart_session and candidate_id:
                cart_session.owner_id = candidate_id
                cart_session.status = 2
                cart_session.save()
                cart_obj = cart_session
            elif cart_session:
                cart_obj = cart_session
            elif candidate_id:
                cart_obj = Cart.objects.create(owner_id=candidate_id, session_id=sessionid, status=2)
            elif sessionid:
                cart_obj = Cart.objects.create(session_id=sessionid, status=0)

            # update cart_obj in session
            if cart_obj:
                request.session.update({
                    "cart_pk": cart_obj.pk,
                    "checkout_type": 'cart',
                    "cart_count_pk": cart_obj.pk,
                })

            elif request.session.get('cart_pk'):
                del request.session['cart_pk']
                del request.session['checkout_type']
                request.session.modified = True
            return cart_obj

        except Exception as e:
            logging.getLogger('error_log').error(str(e))

    def get_cart_items(self, cart_obj=None):
        cart_items = []
        try:
            if not cart_obj:
                if not self.request.session.get('cart_pk'):
                    self.getCartObject()
                cart_pk = self.request.session.get('cart_pk')
                cart_obj = Cart.objects.get(pk=cart_pk)
            if cart_obj:
                main_products = cart_obj.lineitems.filter(parent=None).select_related('product', 'product__vendor')
                for m_prod in main_products:
                    data = {}
                    data['li'] = m_prod
                    data['addons'] = cart_obj.lineitems.filter(parent=m_prod, parent_deleted=False).select_related(
                        'product')
                    data['variations'] = cart_obj.lineitems.filter(parent=m_prod, parent_deleted=True).select_related(
                        'product')
                    cart_items.append(data)
            return cart_items
        except Exception as e:
            logging.getLogger('error_log').error('unable to fetch cart items  %s' % str(e))
        return cart_items

    def get_solr_cart_items(self, cart_obj: object = None) -> object:
        cart_items = []
        total_amount = Decimal(0)
        if not cart_obj:
            if not self.request.session.get('cart_pk'):
                self.getCartObject()
            cart_pk = self.request.session.get('cart_pk')
            cart_obj = Cart.objects.filter(pk=cart_pk).first()
        if cart_obj:
            main_products = cart_obj.lineitems.filter(parent=None)

            main_product_pks = list(main_products.values_list('product__id', flat=True))
            filtered_sqs = SearchQuerySet().filter(id__in=main_product_pks)

            for m_prod in main_products:
                addon_list = []
                combo_list = []
                var_list = []

                try:
                    sqs = filtered_sqs.filter(id=m_prod.product.pk)
                    sqs = sqs[0]
                    main_id = m_prod.id
                    product_class = sqs.pPc
                    name = sqs.pHd if sqs.pHd else sqs.pNm
                    vendor_name = sqs.pPvn
                    price = round(Decimal(sqs.pPinb), 2)
                    delivery_obj = m_prod.delivery_service
                    is_available = True
                    experience = sqs.pEX
                    reference = m_prod.reference

                    addons = cart_obj.lineitems.filter(parent=m_prod, parent_deleted=False).select_related('product')
                    variations = cart_obj.lineitems.filter(parent=m_prod, parent_deleted=True).select_related('product')

                    if m_prod.no_process and product_class == 'course' and variations:
                        pass
                    elif is_available:
                        total_amount += price

                    if m_prod.delivery_service and is_available:
                        total_amount += m_prod.delivery_service.get_price()

                    sqs_vars = json.loads(sqs.pVrs).get('var_list', [])
                    deleted = False
                    for var in variations:
                        found = False
                        for sqs_var in sqs_vars:
                            if sqs_var.get('id') == var.product.id:
                                var_id = var.id
                                var_name = sqs_var.get('label')
                                var_price = round(Decimal(sqs_var.get('inr_price')), 2)
                                var_available = True if is_available else False
                                var_exp = sqs_var.get('experience')
                                var_delivery_obj = var.delivery_service
                                var_reference = var.reference

                                found = True
                                if var_available:
                                    total_amount += var_price

                                if is_available and var.delivery_service:
                                    total_amount += var.delivery_service.get_price()

                                var_data = {
                                    "id": var_id,
                                    "li": var,
                                    "name": var_name,
                                    "price": var_price,
                                    "is_available": var_available,
                                    "experience": var_exp,
                                    "delivery_obj": var_delivery_obj,
                                    "reference": var_reference,
                                }

                                var_list.append(var_data)
                                break
                        if not found:
                            deleted = True
                            var.delete()

                    if deleted and not cart_obj.lineitems.filter(parent=m_prod, parent_deleted=True).exists():
                        m_prod.delete()
                        continue

                    sqs_addons = json.loads(sqs.pFBT).get('fbt_list', [])
                    for addon in addons:
                        found = False
                        for sqs_addon in sqs_addons:
                            if sqs_addon.get('id') == addon.product.id:
                                addon_id = addon.id
                                addon_name = sqs_addon.get('label')
                                addon_price = round(Decimal(sqs_addon.get('inr_price')), 2)
                                addon_available = True if is_available else False
                                addon_exp = sqs_addon.get('experience')
                                addon_reference = addon.reference
                                found = True
                                if addon_available:
                                    total_amount += addon_price

                                addon_data = {
                                    "id": addon_id,
                                    "li": addon,
                                    "name": addon_name,
                                    "price": addon_price,
                                    "is_available": addon_available,
                                    "experience": addon_exp,
                                    "reference": addon_reference,
                                }

                                addon_list.append(addon_data)
                                break
                        if not found:
                            addon.delete()

                    combo_list = json.loads(sqs.pCmbs).get('combo_list', [])

                    data = {
                        "id": main_id,
                        "li": m_prod,
                        "product_class": product_class,
                        "vendor": vendor_name,
                        "name": name,
                        "price": price,
                        "experience": experience,
                        "reference": reference,
                        "delivery_obj": delivery_obj,
                        "addons": addon_list,
                        "variations": var_list,
                        "combos": combo_list,
                        "is_available": is_available,
                        "delivery_types": m_prod.product.get_delivery_types(),
                    }
                    cart_items.append(data)

                except Exception as e:
                    logging.getLogger('error_log').error("Unable to add item on cart %s " % str(e))
                    m_prod.delete()

        return {"cart_items": cart_items, "total_amount": round(total_amount, 2)}

    #  get the child variants of a product in case of resume builder
    def get_variant_list(self, variations, total_amount, is_available, var_list):
        for var in variations:
            var_id = var.id
            var_name = var.product.name
            var_price = round(Decimal(var.price_excl_tax), 2)
            var_available = True if is_available else False
            var_exp = ''
            var_delivery_obj = var.delivery_service
            var_reference = var.reference

            if var_available:
                total_amount += var_price

            if is_available and var.delivery_service:
                total_amount += var.delivery_service.get_price()

            var_data = {
                "id": var_id,
                "li": var,
                "name": var_name,
                "price": var_price,
                "is_available": var_available,
                "experience": var_exp,
                "delivery_obj": var_delivery_obj,
                "reference": var_reference,
            }

            var_list.append(var_data)

        return total_amount, var_list

    # add the product to the cart in case of resume builder
    def add_item_to_cart(self, main_products: object, products: object, cart_obj: object, cart_items: object,
                         total_amount: object) -> object:
        # import ipdb ; ipdb.set_trace()

        for m_prod in main_products:
            addon_list = []
            combo_list = []
            var_list = []
            sqs = products.filter(id=m_prod.product.pk).first()
            if not (sqs):
                continue
            main_id = m_prod.id
            product_class = sqs.product_class.name
            name = sqs.name
            vendor_name = sqs.vendor.name
            price = round(Decimal(sqs.get_price()), 2)
            delivery_obj = m_prod.delivery_service
            experience = ''
            is_available = True
            reference = m_prod.reference

            variations = cart_obj.lineitems.filter(parent=m_prod, parent_deleted=True).select_related('product')

            if m_prod.no_process and product_class == 'course' and variations:
                pass
            elif is_available:
                total_amount += price

            if m_prod.delivery_service and is_available:
                total_amount += m_prod.delivery_service.get_price()

            total_amount, var_list = self.get_variant_list(variations, total_amount, is_available, var_list)

            data = {
                "id": main_id,
                "li": m_prod,
                "product_class": product_class,
                'type_flow': m_prod.product.type_flow,
                "vendor": vendor_name,
                "name": name,
                "price": price,
                "experience": experience,
                "reference": reference,
                "delivery_obj": delivery_obj,
                "addons": addon_list,
                "variations": var_list,
                "combos": combo_list,
                "is_available": is_available,
                "delivery_types": m_prod.product.get_delivery_types(),
            }
            cart_items.append(data)

        return cart_items, total_amount

    # use local db not solar for fetching items in case of resume builder
    def get_local_cart_items(self, cart_obj: object = None) -> object:
        cart_items = []
        total_amount = Decimal(0)
        if not cart_obj:
            if not self.request.session.get('cart_pk'):
                self.getCartObject()
            cart_pk = self.request.session.get('cart_pk')
            cart_obj = Cart.objects.filter(pk=cart_pk).first()
            return {"cart_items": cart_items, "total_amount": round(total_amount, 2)}

        main_products = cart_obj.lineitems.filter(parent=None)

        main_product_pks = list(main_products.values_list('product__id', flat=True))

        products = Product.objects.filter(id__in=main_product_pks).select_related('product_class', 'vendor')

        cart_items, total_amount = self.add_item_to_cart(main_products, products, cart_obj, cart_items, total_amount)

        return {"cart_items": cart_items, "total_amount": round(total_amount, 2)}

    def getTotalAmount(self, cart_obj=None):
        total = Decimal(0)
        try:
            if not cart_obj:
                if not self.request.session.get('cart_pk'):
                    self.getCartObject()
                cart_pk = self.request.session.get('cart_pk')
                cart_obj = Cart.objects.get(pk=cart_pk)
            if cart_obj:
                lis = cart_obj.lineitems.filter(no_process=False).select_related('product')
                for li in lis:
                    total += li.product.get_price()
                lis = cart_obj.lineitems.filter(no_process=True).select_related('product')
                for li in lis:
                    if li.product.is_course and li.no_process == True:
                        pass
                    else:
                        total += li.product.get_price()
                lis_with_delivery = cart_obj.lineitems.all().exclude(delivery_service=None)
                for li in lis_with_delivery:
                    if li.delivery_service:
                        total += li.delivery_service.get_price()
            return round(total, 0)
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return round(total, 0)

    def getPayableAmount(self, cart_obj, total_amount=Decimal(0)):
        total_amount = total_amount
        total_payable_amount = Decimal(0)
        tax_amount = Decimal(0)
        coupon_amount = Decimal(0)
        redeemed_reward_point = Decimal(0)
        amount_after_discount = Decimal(0)
        tax_rate_per = settings.TAX_RATE_PERCENTAGE
        try:
            if not cart_obj:
                if not self.request.session.get('cart_pk'):
                    self.getCartObject()
                cart_pk = self.request.session.get('cart_pk')
                cart_obj = Cart.objects.get(pk=cart_pk)
            if cart_obj:
                if not total_amount:

                    # cart_dict = self.get_solr_cart_items(cart_obj=cart_obj)
                    line_item = cart_obj.lineitems.filter(parent=None)[0]
                    type_flow = int(line_item.product.type_flow)
                    # resume builder flow handle
                    if type_flow == 16:
                        cart_dict = self.get_local_cart_items(cart_obj=cart_obj)
                    else:
                        cart_dict = self.get_solr_cart_items(cart_obj=cart_obj)
                    total_amount = cart_dict.get('total_amount', Decimal(0))

                total_amount = InvoiceGenerate().get_quantize(total_amount)
                coupon_obj = cart_obj.coupon
                wal_txn = cart_obj.wallettxn.filter(txn_type=2).order_by('-created').select_related('wallet')
                valid_coupon = False
                if coupon_obj:
                    valid_coupon = coupon_obj.is_valid_coupon(
                        site=1, source=None, cart_obj=cart_obj)
                if valid_coupon and coupon_obj.coupon_type == 'flat':
                    coupon_amount = coupon_obj.value
                elif valid_coupon and coupon_obj.coupon_type == 'percent':
                    coupon_amount = (total_amount * coupon_obj.value) / 100
                    coupon_amount = InvoiceGenerate().get_quantize(coupon_amount)
                elif wal_txn.exists():
                    wal_txn = wal_txn[0]
                    redeemed_reward_point = wal_txn.point_value

                if not valid_coupon and coupon_obj:
                    try:
                        user_coupon = coupon_obj.users.get(
                            user=cart_obj.email)
                        user_coupon.redeemed_at = None
                        user_coupon.save()
                        cart_obj.coupon = None
                        cart_obj.save()
                    except:
                        cart_obj.coupon = None
                        cart_obj.save()

                if coupon_amount >= total_amount:
                    coupon_amount = total_amount

                if redeemed_reward_point >= total_amount:
                    redeemed_reward_point = total_amount

                amount_after_discount = total_amount

                if coupon_amount:
                    amount_after_discount = amount_after_discount - coupon_amount

                elif redeemed_reward_point:
                    amount_after_discount = amount_after_discount - redeemed_reward_point

                tax_amount = Decimal(0)
                try:
                    if cart_obj.country and cart_obj.country.phone == '91':
                        tax_amount = (amount_after_discount * tax_rate_per) / 100
                        tax_amount = InvoiceGenerate().get_quantize(tax_amount)

                except Exception as e:
                    logging.getLogger('error_log').error("Cart object has no country attached:", str(e))
                total_payable_amount = amount_after_discount + tax_amount
        except Exception as e:
            logging.getLogger('error_log').error(str(e))

        data = {
            "total_amount": total_amount,
            "tax_amount": tax_amount,
            "total_payable_amount": total_payable_amount,
            "tax_rate_per": tax_rate_per,
            "coupon_amount": coupon_amount,
            "amount_after_discount": amount_after_discount,
            "redeemed_reward_point": redeemed_reward_point,
        }
        data.update(
            InvoiceGenerate().getTaxAmountByPart(
                tax_amount, tax_rate_per, cart_obj=cart_obj))
        return data

    def getSelectedProduct(self, product):
        data = {'selected_products': []}
        if not self.request.session.get('cart_pk'):
            self.getCartObject()
        cart_pk = self.request.session.get('cart_pk')
        if cart_pk:
            try:
                cart_obj = Cart.objects.get(pk=cart_pk)
                parent_li = cart_obj.lineitems.get(
                    product=product)
            except Exception as e:
                # logging.getLogger('error_log').error(str(e))
                parent_li = None
            if parent_li:
                selected_product = cart_obj.lineitems.filter(parent=parent_li).values_list('product__pk', flat=True)
                data['selected_products'] = selected_product
        return data

    def getSelectedProduct_solr(self, sqs):
        data = {'selected_products': []}
        if not self.request.session.get('cart_pk'):
            self.getCartObject()
        cart_pk = self.request.session.get('cart_pk')
        if cart_pk:
            try:
                cart_obj = Cart.objects.get(pk=cart_pk).prefetch_related('lineitems')
                product = Product.objects.get(id=sqs.id)
                parent_li = cart_obj.lineitems.get(product=product)
            except Exception as e:
                # logging.getLogger('error_log').error("Unable to select product, {},{}".format(str(e), cart_pk))
                parent_li = None
            if parent_li:
                selected_product = cart_obj.lineitems.filter(parent=parent_li).values_list('product__pk', flat=True)
                data['selected_products'] = selected_product
        return data

    def getSelectedProductPrice(self, product):
        data = {}
        total = Decimal(0)
        fake_total = Decimal(0)
        if not self.request.session.get('cart_pk'):
            self.getCartObject()
        cart_pk = self.request.session.get('cart_pk')
        if cart_pk:
            try:
                cart_obj = Cart.objects.get(pk=cart_pk)
                parent_li = cart_obj.lineitems.get(product=product)
                if parent_li and parent_li.product.is_course and parent_li.no_process == True:
                    pass
                elif parent_li:
                    total += parent_li.product.get_price()
                    if parent_li.product.get_fakeprice():
                        fake_total += parent_li.product.get_fakeprice()[0]
                    else:
                        fake_total += parent_li.product.get_price()
            except Exception as e:
                # logging.getLogger('error_log').error(str(e))
                parent_li = None
            if parent_li:
                lis = cart_obj.lineitems.filter(parent=parent_li).select_related('product')
                for li in lis:
                    total += li.product.get_price()
                    if li.product.get_fakeprice():
                        fake_total += li.product.get_fakeprice()[0]
                    else:
                        fake_total += li.product.get_price()
        if fake_total > Decimal(0.00):
            diff = fake_total - total
            percent_diff = round((diff / fake_total) * 100, 0)
            data.update({'percent_diff': percent_diff, })

        data.update({
            "product_total_price": round(total, 0),
            "fake_total": round(fake_total, 0)})
        return data

    def getSelectedProductPrice_solr(self, sqs):
        data = {}
        total = Decimal(0)
        fake_total = Decimal(0)
        if not self.request.session.get('cart_pk'):
            self.getCartObject()
        cart_pk = self.request.session.get('cart_pk')
        if cart_pk:
            try:
                cart_obj = Cart.objects.get(pk=cart_pk)
                product = Product.objects.get(id=sqs.id)
                parent_li = cart_obj.lineitems.get(product=product)
                if parent_li and parent_li.product.is_course and parent_li.no_process == True:
                    pass
                elif parent_li:
                    total += parent_li.product.get_price()
                    if parent_li.product.get_fakeprice():
                        fake_total += parent_li.product.get_fakeprice()[0]
                    else:
                        fake_total += parent_li.product.get_price()
            except Exception as e:
                # logging.getLogger('error_log').error(str(e))
                parent_li = None
            if parent_li:
                lis = cart_obj.lineitems.filter(parent=parent_li).select_related('product')
                for li in lis:
                    total += li.product.get_price()
                    if li.product.get_fakeprice():
                        fake_total += li.product.get_fakeprice()[0]
                    else:
                        fake_total += li.product.get_price()
        if fake_total > Decimal(0.00):
            diff = fake_total - total
            percent_diff = round((diff / fake_total) * 100, 0)
            data.update({'percent_diff': percent_diff, })

        data.update({
            "product_total_price": round(total, 0),
            "fake_total": round(fake_total, 0)})
        return data

    def get_cart_count(self, request=None):
        total_count = 0
        try:
            if not request:
                request = self.request
            if not request.session.get('cart_count_pk'):
                self.getCartObject(request=request)
            cart_pk = request.session.get('cart_count_pk')

            if cart_pk:

                course_classes = ProductClass.objects.filter(
                    slug__in=settings.COURSE_SLUG)

                cart_obj = Cart.objects.filter(pk=cart_pk).first()
                if cart_obj and cart_obj.status in [0, 2]:
                    total_count += cart_obj.lineitems.all().count()
                    total_count -= cart_obj.lineitems.filter(Q(parent=None, product__product_class__in=course_classes,
                                                               no_process=True) |
                                                             Q(parent=None, product__type_flow=16,
                                                               no_process=True)).count()
        except Exception as e:
            logging.getLogger('error_log').error("{},{}".format(str(e), cart_pk))
        return total_count

    def closeCartObject(self, cart_obj=None):
        if cart_obj:
            # update cart status
            last_status = cart_obj.status
            cart_obj.status = 5
            cart_obj.last_status = last_status
            cart_obj.date_closed = timezone.now()
            cart_obj.save()
