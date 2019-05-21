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
    month = val / 30.0
    if month < 1:
        month = math.ceil(month)
        return str(month) + ' month'
    else:
        month = round(month)
    if month > 12:
        year = round(month / 12)
        if year == 1:
            return str(year) + ' year'
        else:
            return str(year) + ' years'
    return str(month) + ' months'

@register.filter(name='get_value_from_dict')
def get_value_from_dict(value, key):
    if value:
        value = value[0]
        value = eval(value)
        return value[key]
