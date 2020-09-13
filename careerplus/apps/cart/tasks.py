# In-built python
import logging
import json
import datetime
from datetime import timedelta
from decimal import Decimal

# Django imports
from django.conf import settings
from django.utils import timezone
from django.core.cache import cache

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
from payment.tasks import make_logging_request

time_delta = 45 if not settings.DEBUG else 0

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
def cart_drop_out_mail(pk=None, cnd_email=None, mail_type=None, name=None, 
    tracking_id="", u_id="", tracking_product_id="", 
    product_tracking_mapping_id="", trigger_point="", 
    position=-1, utm_campaign="", domain=2):
    mail_type = 'CART_DROP_OUT' if not mail_type else mail_type
    cart_objs = Cart.objects.filter(
        status=2,
        shipping_done=False,
        payment_page=False,
        owner_id__isnull=False, pk=pk).exclude(owner_id__exact='')
    count = 0
    for crt_obj in cart_objs:
        # send mail only if user has not edited cart in the last 45 minutes 
        if crt_obj.modified < (timezone.now()- timezone.timedelta(minutes=time_delta)):
            cart_id = crt_obj.owner_id
            data = {}
            last_cart_items = []
            to_email, toemail = [], ""
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

                name = name if name else "Candidate"
                data['name'] = name
                if mail_type == "SHINE_CART_DROP":
                    subject_name = "{}, ".format(name) if name != 'Candidate' else ''
                    data.update({
                        'subject' : "{}Your cart is waiting!".format(subject_name)
                        })
                    email_list_spent = cache.get("email_sent_for_the_day", [])
                    if toemail in email_list_spent: 
                        logging.getLogger('info_log').info(
                            "Candidate already recieved an email for the day, email: {}".format(to_email))
                        continue
                    else:
                        email_list_spent.append(toemail)
                        cache.set("email_sent_for_the_day", email_list_spent)
                        if product_tracking_mapping_id and tracking_id and tracking_product_id:
                                make_logging_request.delay(
                                        tracking_product_id, product_tracking_mapping_id, tracking_id,\
                                         'exit_cart_mail_sent', position, trigger_point, u_id, utm_campaign, domain)

                token = AutoLogin().encode(toemail, cart_id, days=None)
                data['autologin'] = "{}://{}/cart/payment-summary/?t_id={}&token={}&utm_campaign=learning_exit_mailer&trigger_point={}&u_id={}&position={}&emailer=1&t_prod_id={}&prod_t_m_id={}".format(
                    settings.SITE_PROTOCOL, settings.SITE_DOMAIN, tracking_id, token,trigger_point, u_id, position, tracking_product_id, product_tracking_mapping_id)
                if domain == 3:
                    data.update({
                        'autologin' : "{}://{}/cart/payment-summary/?t_id={}&utm_campaign=learning_exit_mailer&trigger_point={}&u_id={}&position={}&emailer=1&t_prod_id={}&prod_t_m_id={}".format(
                    settings.SITE_PROTOCOL, settings.RESUME_SHINE_SITE_DOMAIN, tracking_id, trigger_point, u_id, position, tracking_product_id, product_tracking_mapping_id)
                        })

                try:
                    SendMail().send(to_email, mail_type, data)
                    count += 1
                except Exception as e:
                    logging.getLogger('error_log').error(
                        "{}-{}-{}".format(
                            str(to_email), str(mail_type), str(e)))
    print("{} of {} cart dropout mails sent".format(count, cart_objs.count()))

@task(name="cart_product_removed_mail")
def cart_product_removed_mail(product_id= None, tracking_id="", 
        u_id=None, email=None, name=None, tracking_product_id="", 
        product_tracking_mapping_id="", trigger_point="", 
        position=-1, utm_campaign="", domain=2):
    try:
        name = name if name else "Candidate"
        if not email and not u_id:
            logging.getLogger('error_log').error(
                "Email is not present, email: {}".format(email))
            return
        mail_type = 'CART_FUNNEL_DROP'

        email_list_spent = cache.get("email_sent_for_the_day", [])
        if email in email_list_spent:
            logging.getLogger('info_log').info(
                "Candidate already recieved an email for the day, email: {}".format(email))
            return

        to_email = [email]
        try: 
            prod = Product.objects.filter(id=product_id).first()
        except Exception as e:
            logging.getLogger('error_log').error("product does not exist: {}".format(product_id))
            return

        data = dict()
        data['name'] = name
        data['product_name'] = prod.heading
        data['product_url'] = prod.url
        data['product_price'] = round(prod.inr_price, 2)
        data['product_description'] = prod.meta_desc
        subject_name = "{}, ".format(name) if name != "Candidate" else ""
        data['subject'] = '{}Forgot Something?'.format(subject_name)

        token = AutoLogin().encode(email, u_id, days=None)
        data['autologin'] = "{}://{}/cart/payment-summary/?prod_id={}&t_id={}&token={}&utm_campaign=learning_remove_product_mailer&trigger_point={}&u_id={}&position={}&email=1".format(
            settings.SITE_PROTOCOL, settings.SITE_DOMAIN, product_id, tracking_id, token, trigger_point, u_id, position)
        if domain == 3:
            data.update({
                'autologin' : "{}://{}/cart/payment-summary/?prod_id={}&t_id={}&utm_campaign=learning_remove_product_mailer&trigger_point={}&u_id={}&position={}&email=1".format(
            settings.SITE_PROTOCOL, settings.RESUME_SHINE_SITE_DOMAIN, product_id, tracking_id, trigger_point, u_id, position)
                })


        email_list_spent.append(email)
        cache.set("email_sent_for_the_day", email_list_spent)
        try:
            SendMail().send(to_email, mail_type, data)
            logging.getLogger('info_log').info("cart product removed mail successfully sent {}".format(email))
        except Exception as e:
            logging.getLogger('error_log').error("Unable to sent mail: {}".format(e))
        make_logging_request.delay(
            tracking_product_id, product_tracking_mapping_id, tracking_id, 'remove_product_mail_sent', position, trigger_point, u_id, utm_campaign, domain)
    except Exception as e:
         logging.getLogger('error_log').error(e)



