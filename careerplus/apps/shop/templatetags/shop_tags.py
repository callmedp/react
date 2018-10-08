from django import template                                                                      

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
def ordinal_number(val):
    return "%d%s" % (val,"tsnrhtdd"[(val/10%10!=1)*(val%10<4)*val%10::4])