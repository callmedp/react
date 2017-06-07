from django import template                                                                      
register = template.Library()

@register.filter
def get_instance(form_set):
    try:
        return str(form_set.instance)
    except:
        pass    
    return False
