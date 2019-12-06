from django import template      
from django.utils.html import strip_tags                                                                
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
        return value.get(key,'')


''' this fucntion is to convert the string data in the format
    eg. '<p><strong>.....</strong></p><p>m...</p> <p><strong>.....</strong></p><p>m...</p> <p><strong>.....</strong></p><p>m...</p>'
    to a list with heading and content like this
    [{heading:`<p><strong>.....</strong></p>`, content:`<p>m...</p>}`,....]

'''
@register.filter(name='get_faq_list')
def get_faq_list(string):
    list_data = [i for i in string.split('\n') if not i.find('<p>')==-1]
    return [{'heading':list_data[i],'content':list_data[i+1]} if len(list_data) >i+1 \
                else {'heading':list_data[i]} for i in range(0,len(list_data),2)]

'''
this function is to convert the description into a list 
'''
@register.filter(name='format_description')
def format_description(string):
    return  [strip_tags(i) + '</br></br>' for i in string.split('\n') if not i.find('<p>')==-1]








