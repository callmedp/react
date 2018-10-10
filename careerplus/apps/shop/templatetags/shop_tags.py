from django import template                                                                      
import math
register = template.Library()


@register.filter(name='get_value')
def get_value(key, dictionary):
    return dictionary.get(key, [])


@register.filter
def get_eval_value(val):
    return eval(val)


@register.filter(name='split')
def split(value, arg):
    return value.split(arg)


@register.filter
def convert_to_month(val):
    return math.ceil(val / 30.0)
