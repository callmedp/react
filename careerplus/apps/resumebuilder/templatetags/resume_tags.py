from django import template
register = template.Library()

@register.filter
def length(arr, i):
    return len(arr)