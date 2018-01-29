from django import template                                                                      

register = template.Library()


@register.filter(name='get_value')
def get_value(key, dictionary):
    return dictionary.get(key, [])
