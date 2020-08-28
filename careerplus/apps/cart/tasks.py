# In-built python
import logging
import json
import datetime
from datetime import timedelta
from decimal import Decimal

# Django imports
from django.conf import settings
from django.utils import timezone

# Third party imports
from celery.decorators import task

# Local imports
# from order.functions import date_timezone_convert
from cart.models import Cart
from shop.models import Product
from emailers.email import SendMail
from crmapi.functions import lead_create_on_crm
from cart.mixins import CartMixin
from linkedin.autologin import AutoLogin


@task(name="create_lead_on_crm")
def create_lead_on_crm(pk=None, source_type=None, name=None):
    cart_lead_creation_dict = {
        "cart_drop_out": {"shipping_done": False,
                          "payment_page": False,
                          },
        "shipping_drop_out": {"shipping_done": True,
                              "payment_page": False,
                             },
        "payment_drop_out": {"shipping_done": True,
                             "payment_page": True,
                             }

    }
    source_in_dict = cart_lead_creation_dict.get(source_type,None)
    if not source_in_dict:
        return
    filter_dict = {'status': 2, 'owner_id__isnull': False, 'pk': pk}
    filter_dict.update(source_in_dict)
    lead_creation_function(filter_dict=filter_dict, cndi_name=name)


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
            lead_type = 1
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
            deltatasktime = timezone.now() - timedelta(seconds=settings.CART_DROP_OUT_LEAD)
            # deltatasktime = date_timezone_convert(deltatasktime)  if timezone is needed
            server_time = deltatasktime
            prod = m_prods.filter(modified__lte=server_time).first()
            counter = 0
            if prod:
                # logging.getLogger('error_log').error('prdid'+ str(prod.id))
                logging.getLogger('info_log').info("lead creation process for product-"+str(prod.id))
                counter += 1
                product_name = prod.product.heading if prod.product.heading else prod.product.name
                data_dict.update({
                                     "product": product_name,
                                     "productid": prod.product.id
                                 })
                m_prods = m_prods.exclude(id=prod.id)
            for m_prod in m_prods:
                # logging.getLogger('error_log').error('inside the loop')

                if counter == 0:
                    product_name = m_prod.product.heading if m_prod.product.heading else m_prod.product.name
                    data_dict.update({
                        "product": product_name,
                        "productid": m_prod.product.id
                    })
                    counter += 1
                    continue
                product_name = m_prod.product.heading if m_prod.product.heading else m_prod.product.name
                # logging.getLogger('error_log').error('innerprod'+str(m_prod.id))

                product_list.append(product_name)
                addons = cart_obj.lineitems.filter(
                    parent=m_prod,
                    parent_deleted=False
                ).select_related('product')

                variations = cart_obj.lineitems.filter(
                    parent=m_prod,
                    parent_deleted=True
                ).select_related('product')
                for addon in addons:
                    addon = addon.product.heading if addon.product.heading else addon.product.name
                    addon_list.append(addon)
                for variation in variations:
                    variation = variation.product.heading if variation.product.heading else variation.product.name
                    variation_list.append(variation)
                extra_info.update({
                    "parent": product_list,
                    "addon": addon_list,
                    "variation": variation_list
                })
            if m_prods and m_prods.count() == 1:
                m_prod = m_prods[0]
            
            data_dict.update({"extra_info": json.dumps(extra_info)})

            #Create resume lead if resume items present in cart
            if cart_obj.lineitems.exclude(product__type_flow__in=[2,14,16]):
                data_dict.update({
                    "campaign_slug": "cartleads",
                    'lead_type': lead_type,
                })
                # create lead on crm
                lead_create_on_crm(cart_obj, data_dict=data_dict)
            
            if not cart_obj.lineitems.filter(product__type_flow__in=[2,14,16]):
                return

            #Create course lead if course items present in cart
            data_dict.update({
                    "campaign_slug":"cartleadcourses",
                    "lead_type":2
                    })
            lead_create_on_crm(cart_obj, data_dict=data_dict)
    
    except Exception as e:
        logging.getLogger('error_log').error("lead creation from crm failed %s" % str(e))


@task(name="cart_drop_out_mail")
def cart_drop_out_mail(pk=None, cnd_email=None):
    import ipdb;ipdb.set_trace();
    mail_type = 'CART_DROP_OUT'
    cart_objs = Cart.objects.filter(
        status=2,
        shipping_done=False,
        payment_page=False,
        owner_id__isnull=False, pk=pk).exclude(owner_id__exact='')
    count = 0
    for crt_obj in cart_objs:
        # send mail only if user has not edited cart in the last 45 minutes 
        if crt_obj.modified < (timezone.now()- timezone.timedelta(minutes=45)):
            cart_id = crt_obj.owner_id
            data = {}
            last_cart_items = []
            to_email = []
            total_price = Decimal(0)
            m_prod = crt_obj.lineitems.filter(
                parent=None).select_related(
                'product', 'product__vendor').order_by('-created')
            if len(m_prod):
                m_prod = m_prod[:2]
                for parent in m_prod:
                    product_dict = dict()
                    product_dict['m_prod'] = parent
                    product_dict['addons'] = crt_obj.lineitems.filter(
                        parent=parent,
                        parent_deleted=False).select_related('product')
                    product_dict['variations'] = crt_obj.lineitems.filter(
                        parent=parent,
                        parent_deleted=True).select_related('product')
                    product_name = parent.product.heading if parent.product.heading else parent.product.name
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
                data['autologin'] = "{}://{}/autologin/{}/?next=/cart/payment_summary".format(
                    settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                    token)
                try:
                    SendMail().send(to_email, mail_type, data)
                    count += 1
                except Exception as e:
                    logging.getLogger('error_log').error(
                        "{}-{}-{}".format(
                            str(to_email), str(mail_type), str(e)))
    print("{} of {} cart dropout mails sent".format(count, cart_objs.count()))

@task(name="cart_product_removed_mail")
def cart_product_removed_mail(data):
    cart_id = data.get('card_id', '')
    email = data.get('email', '')
    prod_id = data.get('prod_id', '')
    mail_type = 'CART_DROP_OUT'
    last_cart_items = []
    cart_obj = Cart.objects.filter(
        status=2,
        shipping_done=False,
        payment_page=False,
        owner_id__isnull=False, 
        pk=cart_id).exclude(owner_id__exact='').first()
    count = 0

    if cart_obj.modified < (timezone.now()- timezone.timedelta(minutes=30))\
        and len(cart_obj.lineitems.all()) == 0:
        cart_id = crt_obj.owner_id
        data = {}
        last_cart_items = []
        to_email = [email]
        total_price = Decimal(0)
        prod = Product.object.filter(id=prod_id).first()

        product = dict()
        product['name'] = prod.name


        token = AutoLogin().encode(toemail, cart_id, days=None)
        data['autologin'] = "{}://{}/autologin/{}/?next=/cart/payment_summary".format(
            settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token)



