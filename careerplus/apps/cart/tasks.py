import logging
import json
from celery.decorators import task
from django.conf import settings
from cart.models import Cart
from emailers.email import SendMail
from crmapi.functions import lead_create_on_crm
from cart.mixins import CartMixin
from shine.core import ShineCandidateDetail
from linkedin.autologin import AutoLogin


@task(name="create_lead_on_crm")
def create_lead_on_crm(source_type=None):
    try:
        filter_dict = {}
        if source_type == "cart_drop_out":
            filter_dict.update({
                "status": 2,
                "owner_id__isnull": False,
                "shipping_done": False,
                "payment_page": False,
            })
            lead_creation_function(filter_dict=filter_dict)

        if source_type == "shipping_drop_out":
            filter_dict.update({
                "status": 2,
                "owner_id__isnull": False,
                "shipping_done": True,
                "payment_page": False,
            })
            lead_creation_function(filter_dict=filter_dict)

        if source_type == "payment_drop_out":
            filter_dict.update({
                "status": 2,
                "owner_id__isnull": False,
                "shipping_done": False,
                "payment_page": True,
            })
            lead_creation_function(filter_dict=filter_dict)
    except Exception as e:
        logging.getLogger('error_log').error("%s" % str(e))


def lead_creation_function(filter_dict=None):
    try:
        cart_objs = Cart.objects.filter(**filter_dict).exclude(owner_id__exact='')
        extra_info = {}
        for cart_obj in cart_objs:
            data_dict = {}
            total_amount = None
            data_dict.update({
                "name": '{}{}'.format(cart_obj.first_name, cart_obj.last_name),
                "email": cart_obj.email,
                "mobile": cart_obj.mobile,
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
                                parent_delete=False
                            ).select_related('product')

                            variations = cart_obj.lineitems.filter(
                                parent=m_prod,
                                parent_delete=True
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
def cart_drop_out_mail():
    mail_type = 'CART_DROP_OUT'
    cart_objs = Cart.objects.filter(
        status=2,
        owner_id__isnull=False).exclude(owner_id__exact='')
    count = 0
    for cart_obj in cart_objs:
        try:
            crt_obj = cart_obj
            data = {}
            total_amount = None
            last_cart_items = []
            to_email = []
            if crt_obj:
                total_amount = CartMixin().getPayableAmount(cart_obj)
                data['total'] = total_amount.get('total_payable_amount')
                m_prod = crt_obj.lineitems.filter(
                    parent=None, send_email=False).select_related(
                    'product', 'product__vendor').order_by('-created')
                m_prod = m_prod[0] if len(m_prod) else None
                if m_prod:
                    data['m_prod'] = m_prod
                    data['addons'] = crt_obj.lineitems.filter(
                        parent=m_prod,
                        parent_deleted=False).select_related('product')
                    data['variations'] = crt_obj.lineitems.filter(
                        parent=m_prod,
                        parent_deleted=True).select_related('product')
                    last_cart_items.append(data)
                    product_name = m_prod.product.heading if m_prod.product.heading else m_prod.product.name
                    data['subject'] = '{} is ready to checkout'.format(
                        product_name)
                    if m_prod.cart.email and m_prod.cart.owner_id:
                        to_email.append(m_prod.cart.email)
                    else:
                        json_data = ShineCandidateDetail().get_status_detail(
                            email=None, shine_id=m_prod.cart.owner_id)
                        if json_data:
                            to_email.append(json_data['email'])
                        else:
                            logging.getLogger('error_log').error("Error in getting"
                                                                 "response from Shine for id:", m_prod.cart.owner_id)
                            continue
                    token = AutoLogin().encode(
                        m_prod.cart.email, m_prod.cart.owner_id, days=None)

                    data['autologin'] = "{}://{}/autologin/{}/?next=/cart/".format(
                        settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                        token.decode())
                    try:
                        SendMail().send(to_email, mail_type, data)
                        m_prod.send_email = True
                        m_prod.save()
                        count += 1
                    except Exception as e:
                        logging.getLogger('email_log').error(
                            "{}-{}-{}".format(
                                str(to_email), str(mail_type), str(e)))
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
    print("{} of {} cart dropout mails sent".format(count, cart_objs.count()))
