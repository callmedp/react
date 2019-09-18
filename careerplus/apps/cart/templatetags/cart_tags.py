from django import template
register = template.Library()
from cart.models import Cart
import json
from django.core import serializers


@register.filter
def is_free(price):
    return int(price) == 0

@register.filter
def get_count(delivery_service):
    if delivery_service:
        return 3 - int(delivery_service.id)
    return 0

@register.filter
def get_cart_info(request):
    cart_pk = request.session.get('cart_pk','')
    if not cart_pk: 
        return ""
    cart_obj =  Cart.objects.filter(id=cart_pk).first()
    if cart_obj:
        import ipdb;
        ipdb.set_trace()
        return 'name=' + str(cart_obj.first_name) + ' ' + str(cart_obj.last_name) + ',email='+  str(cart_obj.email) + ',country_code='+ str(cart_obj.country_code) + ',mobile='+ str(cart_obj.mobile)
    else: 
        return ""
         