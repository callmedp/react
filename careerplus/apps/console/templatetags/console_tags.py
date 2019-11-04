from django import template                                                                      
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse_lazy, reverse
from console.decorators import flatlist
import logging
register = template.Library()

@register.filter
def get_instance(form_set):
    try:
        return str(form_set.instance)
    except Exception as e:
        logging.getLogger('error_log').error(str(e))
        pass    
    return False

@register.filter
def get_edit_url(form_set):
    try:
        if form_set.instance:
            instance = form_set.instance
            return reverse('console:screenproductvariant-change', kwargs={
                'pk': instance.sibling.pk,
                'parent': instance.main.pk}) 
    except Exception as e:
        logging.getLogger('error_log').error(str(e))
        pass
    return ''

@register.filter
def get_edit_purl(form_set):
    try:
        if form_set.instance:
            instance = form_set.instance
            return reverse('console:productvariant-change', kwargs={
                'pk': instance.sibling.pk,
                'parent': instance.main.pk}) 
    except Exception as e:
        logging.getLogger('error_log').error(str(e))
        pass    
    return ''


@register.filter(name='has_group')
def has_group(user, grp_list):
    if user.is_superuser:
        return True
    groups = user.groups.all().values_list('name', flat=True)
    groups = set(groups)
    
    flat_list = [ll for ll in flatlist(grp_list)]
    flat_list = set(flat_list)
    intersection = flat_list.intersection(groups)

    return True if intersection else False


@register.filter(name='widget_type')
def widget_type(field):
  return field.field.widget.__class__.__name__

@register.filter(name='test_chk')
def test_chk(field):
  return field.field.widget.__class__.__name__


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name='dict_username')
def dict_username(key, dict):
    if key in dict:
        return dict[key].username
    else:
        return ''

@register.filter(name='dict_password')
def dict_password(key, dict):
    if key in dict:
        return dict[key].password
    else:
        return ''

@register.filter(name='profile_status')
def profile_status(key, dict):
    if key in dict:
        return dict[key].profile_status
    else:
        return ''

@register.filter(name='is_whole_refund')
def is_whole_refund(key, refund_dict):
    if key in refund_dict:
        return not bool(refund_dict[key]['total_count'] - refund_dict[key]['refund_count'])
    return False

