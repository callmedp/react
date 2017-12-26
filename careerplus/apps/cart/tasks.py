import logging
import json
from decimal import Decimal
from celery.decorators import task
from django.conf import settings
from cart.models import Cart
from emailers.email import SendMail
from crmapi.functions import lead_create_on_crm
from cart.mixins import CartMixin
from linkedin.autologin import AutoLogin


@task(name="create_lead_on_crm")
def create_lead_on_crm(pk=None, source_type=None, name=None):
    try:
        filter_dict = {}
        if source_type == "cart_drop_out":
            filter_dict.update({
                "status": 2,
                "owner_id__isnull": False,
                "shipping_done": False,
                "payment_page": False,
                "pk": pk,
            })
            lead_creation_function(filter_dict=filter_dict, cndi_name=name)

        if source_type == "shipping_drop_out":
            filter_dict.update({
                "status": 2,
                "owner_id__isnull": False,
                "shipping_done": True,
                "payment_page": False,
                "pk": pk,
            })
            lead_creation_function(filter_dict=filter_dict, cndi_name=name)

        if source_type == "payment_drop_out":
            filter_dict.update({
                "status": 2,
                "owner_id__isnull": False,
                "shipping_done": True,
                "payment_page": True,
                "pk": pk,
            })
            lead_creation_function(filter_dict=filter_dict, cndi_name=name)
    except Exception as e:
        logging.getLogger('error_log').error("%s" % str(e))


def lead_creation_function(filter_dict=None, cndi_name=None):
    try:
        cart_objs = Cart.objects.filter(**filter_dict).exclude(owner_id__exact='')
        extra_info = {}
        for cart_obj in cart_objs:
            data_dict = {}
            total_amount = None
            data_dict.update({
                "name": cndi_name,
                "email": cart_obj.email,
                "mobile": cart_obj.mobile,
                "country_code": cart_obj.country_code,
                "lead_source": 2,
            })
            if cart_obj:
                total_amount = CartMixin().getPayableAmount(cart_obj)
                pay_amount = total_amount.get('total_payable_amount')
                extra_info.update({
                    'total_amount': round(pay_amount)
                })
                m_prods = cart_obj.lineitems.filter(
                    parent=None).select_related(
                    'product', 'product__vendor').order_by('-created')
                product_list = []
                addon_list = []
                variation_list = []
                if m_prods:
                    count = 0
                    for m_prod in m_prods:
                        count = count + 1
                        product_name = m_prod.product.heading if m_prod.product.heading else m_prod.product.name
                        if count == 1:
                            data_dict.update({
                                "product": product_name,
                                "productid": m_prod.product.id
                            })
                        else:
                            product_list.append(product_name)
                            addons = cart_obj.lineitems.filter(
                                parent=m_prod,
                                parent_deleted=False
                            ).select_related('product')

                            variations = cart_obj.lineitems.filter(
                                parent=m_prod,
                                parent_deleted=True
                            ).select_related('product')
                            if addons:
                                for addon in addons:
                                    addon = addon.product.heading if addon.product.heading else addon.product.name
                                    addon_list.append(addon)
                            if variations:
                                for variation in variations:
                                    variation = variation.product.heading if variation.product.heading else variation.product.name
                                    variation_list.append(variation)

                    extra_info.update({
                        "parent": product_list,
                        "addon": addon_list,
                        "variation": variation_list
                    })
            data_dict.update({
                "extra_info": json.dumps(extra_info),
                "campaign_slug": "cartleads"
            })
            # create lead on crm
            lead_create_on_crm(cart_obj, data_dict=data_dict)
    except Exception as e:
        logging.getLogger('error_log').error("%s" % str(e))


@task(name="cart_drop_out_mail")
def cart_drop_out_mail(pk=None, cnd_email=None):
    mail_type = 'CART_DROP_OUT'
    cart_id = None
    cart_objs = Cart.objects.filter(
        status=2,
        shipping_done=False,
        payment_page=False,
        owner_id__isnull=False, pk=pk).exclude(owner_id__exact='')
    count = 0
    for crt_obj in cart_objs:
        # try:
        cart_id = crt_obj.owner_id
        data = {}
        last_cart_items = []
        to_email = []
        total_price = Decimal(0)
        if crt_obj:
            m_prod = crt_obj.lineitems.filter(
                parent=None).select_related(
                'product', 'product__vendor').order_by('-created')
            # m_prod = m_prod[0] if len(m_prod) else None
            if len(m_prod):
                for parent in m_prod:
                    product_dict = dict()
                    product_dict['m_prod'] = parent
                    product_dict['addons'] = crt_obj.lineitems.filter(
                        parent=parent,
                        parent_deleted=False).select_related('product')
                    product_dict['variations'] = crt_obj.lineitems.filter(
                        parent=parent,
                        parent_deleted=True).select_related('product')
                    product_name = m_prod.product.heading if m_prod.product.heading else m_prod.product.name
                    product_dict['product_name'] = product_name
                    last_cart_items.append(product_dict)

                data['products'] = last_cart_items
                for last_cart_item in last_cart_items:
                    parent_li = last_cart_item.get('m_prod')
                    addons = last_cart_item.get('addons')
                    variations = last_cart_item.get('variations')
                    product_price = parent_li.product.get_price()
                    parent_li.price_excl_tax = product_price
                    parent_li.save()

                    if not parent_li.no_process:
                        total_price += parent_li.price_excl_tax
                    for li in addons:
                        product_price = li.product.get_price()
                        li.price_excl_tax = product_price
                        li.save()
                        total_price += li.price_excl_tax
                    for li in variations:
                        product_price = li.product.get_price()
                        li.price_excl_tax = product_price
                        li.save()
                        total_price += li.price_excl_tax
                data['total'] = round(total_price, 2)

                data['subject'] = '{} is ready to checkout'.format(
                    product_name)
                data['product'] = product_name
                if cart_id and (cnd_email or crt_obj.email):
                    toemail = cnd_email or crt_obj.email
                    to_email.append(toemail)
                else:
                    logging.getLogger('error_log').error(
                        "Candidate details not present in cart id:", crt_obj.id)
                    continue

                token = AutoLogin().encode(toemail, cart_id, days=None)
                data['autologin'] = "{}://{}/autologin/{}/?next=/cart/".format(
                    settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                    token.decode())
                try:
                    SendMail().send(to_email, mail_type, data)
                    # m_prod.send_email = True
                    # m_prod.save()
                    count += 1
                except Exception as e:
                    logging.getLogger('email_log').error(
                        "{}-{}-{}".format(
                            str(to_email), str(mail_type), str(e)))
        # except Exception as e:
        #     logging.getLogger('error_log').error(str(e))
    print("{} of {} cart dropout mails sent".format(count, cart_objs.count()))
