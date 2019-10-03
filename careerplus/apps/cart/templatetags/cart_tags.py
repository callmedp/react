from django import template
register = template.Library()
from cart.models import Cart
import json
from django.core import serializers


@register.filter
def is_free(price):
    return int(price) == 0

@register.filter
def get_slug(delivery_service):
    if delivery_service:
       return delivery_service.slug
    return 'normal'

@register.filter
def get_cart_info(request):
    cart_pk = request.session.get('cart_pk','')
    if not cart_pk: 
        return ""
    cart_obj =  Cart.objects.filter(id=cart_pk).first()
    if cart_obj:
        return str(cart_obj.first_name or '') + ' ' + str(cart_obj.last_name or '') + ','+  str(cart_obj.email or '') + ','+ str(cart_obj.country_code or '') + ','+ str(cart_obj.mobile or '')
    else: 
        return ""
         

