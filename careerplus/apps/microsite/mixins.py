import logging

from django.conf import settings
from django.template.loader import select_template

# from shinecp.cart.models import ProductVariation


class CommonMethodMixin(object):

    def get_partner_template(self, partner):
        try:
            template = self.partner_template.format(partner=partner)
            return select_template([template, self.default_template]).name
        except Exception as e:
            logging.getLogger('error_log').error('unable to get partner template%s'%str(e))
            return self.default_template

    def import_dynamically(self, fullpath):
        component_list = fullpath.split('.')
        module = __import__(component_list[0])
        for component in component_list[1:]:
            module = getattr(module, component)
        return module

    def get_user_ip(self, request):
        user_ip = settings.ROUNDONE_DEFAULT_CP_EMAIL
        http_x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        try:
            if http_x_forwarded_for:
                user_ip = http_x_forwarded_for.split(',')[0]
            else:
                user_ip = request.META.get('REMOTE_ADDR')
        except Exception as e:
            logging.getLogger('error_log').error('unable to get user_ip%s' % str(e))
            pass
        return user_ip

    def add_cart_roundone(self):
        order = self.get_or_create_order()
        product_variation = ProductVariation.objects.get(pk=1295)
        try:
            order_items = order.add_order_items(
                product_variation=product_variation, unit=1)
            return True
        except Exception as e:
            logging.getLogger('error_log').error('unable to add order item%s'%str(e))
        return False
