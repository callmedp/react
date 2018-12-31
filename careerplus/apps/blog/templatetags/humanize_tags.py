from django import template
from django.contrib.humanize.templatetags.humanize import naturaltime
register = template.Library()


@register.simple_tag
def get_humanize_date(value):
    value = naturaltime(value)
    value_list = value.split(',')
    if len(value_list) > 1:
        value = value_list[0]
        return value.replace('\xa0', ' ') + ' ' + 'ago'
    else:
        return value.replace('\xa0', ' ')
    # return value
