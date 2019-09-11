from django import template
register = template.Library()


@register.filter
def is_free(price):
    return int(price) == 0

@register.filter
def get_count(delivery_service):
    if delivery_service:
        return 3 - int(delivery_service.id)
    return 0
