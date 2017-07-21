from django import template                                                                      
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse_lazy, reverse


register = template.Library()

@register.filter
def get_instance(form_set):
    try:
        return str(form_set.instance)
    except:
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
    except:
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
    except:
        pass    
    return ''


@register.filter(name='has_group')
def has_group(user, group_name):
    try:
        if user.is_superuser:
            return True
        group = Group.objects.get(name=group_name)
        return True if group in user.groups.all() else False
    except:
        return False
    return False


@register.filter(name='widget_type')
def widget_type(field):
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
        return dict[key].Password
    else:
        return ''

@register.filter(name='profile_status')
def profile_status(key, dict):
    if key in dict:
        return dict[key].profile_status
    else:
        return ''
