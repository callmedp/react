from django import template      
from django.utils.html import strip_tags                                                                
import math,numpy
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

'''
this function is to convert the Features into a list with only 2 items cause of space limit
'''
@register.filter(name='format_features')
def format_features(string):
    return  [strip_tags(i) for i in string.split('\n') if not i.find('<li>')==-1][:2]

@register.filter(name='divide_testimonial_category_group_list_of_lists')
def divide_testimonial_category_group_list_of_lists(testimonialcategory):
    if  len(testimonialcategory)%3 == 1:
        items_to_add = 2
    elif len(testimonialcategory)%3 == 2:
        items_to_add = 1
    else:
        items_to_add = 0
    testimonialcategory.extend([None]*items_to_add)
    testimonialcategory = numpy.array(testimonialcategory)
    testimonialcategory = numpy.reshape(testimonialcategory,(-1,3)).tolist()  #convert testimonial into (x,3) x=len/3
    return testimonialcategory

@register.filter(name='get_initials')
def get_initials(user_name):
    if not user_name:
        return 'US'
    splitted_user_name = user_name.split(' ')[:2]
    initials = ''
    for name in user_name.split(' ')[:2]:
        initials+=name[0]
    return initials.upper()









