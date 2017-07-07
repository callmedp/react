from django import template                                                                      
from django.contrib.auth.models import Group


register = template.Library()

@register.filter
def get_instance(form_set):
    try:
        return str(form_set.instance)
    except:
        pass    
    return False

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


