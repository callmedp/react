from django import template

register = template.Library()

@register.filter(name='slugit')
def slugit(value, arg):
    return str(value) + "-" + str(arg)
