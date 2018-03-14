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
        Daily Cron for last cart item
    """

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        get_last_cart_item()


def get_last_cart_item():
    # mail_type = 'CART_DROP_OUT'
    # cart_objs = Cart.objects.filter(status=2, owner_id__isnull=False).exclude(
    #     owner_id__exact='')
    # count = 0
    # for cart_obj in cart_objs:
    #     try:
    #         crt_obj = cart_obj
    #         data = {}
    #         last_cart_items = []
    #         to_email = []
    #         total_price = Decimal(0)
    #         if crt_obj:
    #             m_prod = crt_obj.lineitems.filter(parent=None, send_email=False).select_related(
    #                 'product', 'product__vendor').order_by('-created')
    #             m_prod = m_prod[0] if len(m_prod) else None
    #             if m_prod:
    #                 data['m_prod'] = m_prod
    #                 data['addons'] = crt_obj.lineitems.filter(
    #                     parent=m_prod,
    #                     parent_deleted=False).select_related('product')
    #                 data['variations'] = crt_obj.lineitems.filter(
    #                     parent=m_prod,
    #                     parent_deleted=True).select_related('product')
    #                 last_cart_items.append(data)
    #                 for last_cart_item in last_cart_items:
    #                     parent_li = last_cart_item.get('m_prod')
    #                     addons = last_cart_item.get('addons')
    #                     variations = last_cart_item.get('variations')
    #                     product_price = parent_li.product.get_price()
    #                     product_tax = product_price * Decimal(18 / 100)
    #                     parent_li.price_incl_tax = product_price + product_tax
    #                     parent_li.save()
    #
    #                     if parent_li.no_process == False:
    #                         total_price += parent_li.price_incl_tax
    #                     for li in addons:
    #                         product_price = li.product.get_price()
    #                         product_tax = product_price * Decimal(18 / 100)
    #                         li.price_incl_tax = product_price + product_tax
    #                         li.save()
    #                         total_price += li.price_incl_tax
    #                     for li in variations:
    #                         product_price = li.product.get_price()
    #                         product_tax = product_price * Decimal(18 / 100)
    #                         li.price_incl_tax = product_price + product_tax
    #                         li.save()
    #                         total_price += li.price_incl_tax
    #                 data['total'] = round(total_price, 2)
    #                 product_name = m_prod.product.heading if m_prod.product.heading else m_prod.product.name
    #                 data['subject'] = '{} is ready to checkout'.format(
    #                     product_name)
    #                 if m_prod.cart.email and m_prod.cart.owner_id:
    #                     to_email.append(m_prod.cart.email)
    #                 else:
    #                     json_data = ShineCandidateDetail().get_status_detail(
    #                         email=None, shine_id=m_prod.cart.owner_id)
    #                     if json_data:
    #                         to_email.append(json_data['email'])
    #                     else:
    #                         logging.getLogger('error_log').error("Error in getting"
    #                                                              "response from Shine for id:", m_prod.cart.owner_id)
    #                         continue
    #                 token = AutoLogin().encode(
    #                     m_prod.cart.email, m_prod.cart.owner_id, days=None)
    #                 data['autologin'] = "{}://{}/autologin/{}/?next=/cart/".format(
    #                     settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
    #                     token.decode())
    #                 try:
    #                     SendMail().send(to_email, mail_type, data)
    #                     m_prod.send_email = True
    #                     m_prod.save()
    #                     count += 1
    #                 except Exception as e:
    #                     logging.getLogger('error_log').error(
    #                         "{}-{}-{}".format(
    #                             str(to_email), str(mail_type), str(e)))
    #     except Exception as e:
    #         logging.getLogger('error_log').error(str(e))
    # print("{} of {} cart dropout mails sent".format(count, cart_objs.count()))
    pass