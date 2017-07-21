from django import template                                                                      
register = template.Library()

@register.filter
def get_instance(form_set):
    try:
        return str(form_set.instance)
    except:
        pass    
    return False


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