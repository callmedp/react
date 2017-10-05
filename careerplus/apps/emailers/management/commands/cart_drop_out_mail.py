import logging
from decimal import Decimal
from django.core.management.base import BaseCommand

from emailers.email import SendMail
from cart.models import Cart
from shine.core import ShineCandidateDetail
from linkedin.autologin import AutoLogin
from django.conf import settings


class Command(BaseCommand):
    """
        Daily Cron for draft reminder mail/Sms
    """

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        get_last_cart_item()


def get_last_cart_item():
    try:
        mail_type = 'CART_DROP_OUT'
        cart_objs = Cart.objects.filter(status__in=[2, 3]).exclude(owner_id=None)
        for cart_obj in cart_objs:
            crt_obj = cart_obj
            data = {}
            last_cart_items = []
            to_email = []
            total_price = Decimal(0)
            if crt_obj:
                m_prod = crt_obj.lineitems.filter(parent=None).select_related(
                    'product', 'product__vendor').order_by('-created')[0]
                data['m_prod'] = m_prod
                data['addons'] = crt_obj.lineitems.filter(parent=m_prod, parent_deleted=False).select_related('product')
                data['variations'] = crt_obj.lineitems.filter(parent=m_prod, parent_deleted=True).select_related('product')
                last_cart_items.append(data)
                for last_cart_item in last_cart_items:
                    parent_li = last_cart_item.get('m_prod')
                    addons = last_cart_item.get('addons')
                    variations = last_cart_item.get('variations')
                    product_price = parent_li.product.get_price()
                    product_tax = product_price * Decimal(18 / 100)
                    parent_li.price_incl_tax = product_price + product_tax
                    parent_li.save()

                    if parent_li.no_process == False:
                        total_price += parent_li.price_incl_tax
                    for li in addons:
                        product_price = li.product.get_price()
                        product_tax = product_price * Decimal(18 / 100)
                        li.price_incl_tax = product_price + product_tax
                        li.save()
                        total_price += li.price_incl_tax
                    for li in variations:
                        product_price = li.product.get_price()
                        product_tax = product_price * Decimal(18 / 100)
                        li.price_incl_tax = product_price + product_tax
                        li.save()
                        total_price += li.price_incl_tax
                data['total'] = round(total_price, 2)
                data['subject'] = 'Product is ready to checkout'
                if m_prod.cart.email and m_prod.cart.owner_id:
                    to_email.append(m_prod.cart.email)
                else:
                    json_data = ShineCandidateDetail().get_status_detail(
                        email=None, shine_id=m_prod.cart.owner_id)
                    to_email.append(json_data['email'])
                token = AutoLogin().encode(m_prod.cart.email, m_prod.cart.owner_id, days=None)
                data['autologin'] = "%s://%s/autologin/%s/?next=payment" % (settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token.decode()) 

                try:
                    SendMail().send(to_email, mail_type, data)

                except Exception as e:
                    logging.getLogger('email_log').error("%s - %s - %s" % (str(to_email), str(mail_type), str(e)))
    except Exception as e:
        logging.getLogger('error_log').error(str(e))