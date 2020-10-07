#python imports
import re
from datetime import datetime

#django imports
from django import template
from django.http import QueryDict
from django.template.defaultfilters import mark_safe

#local imports
from search import choices

#inter app imports

#third party imports
import urllib
import logging

register = template.Library()

@register.filter
def get_choice_display(value, choice):
    """
    Return user displayable value of against a lookup id. Mainly used while
    listing facets but can be used elsewhere
    """
    mapping = dict(getattr(choices, choice))
    if not value or value in mapping:
        return mapping.get(value, 'Others')
    if value.isdigit():
        value = int(value)
    elif value.lower() in mapping:
        value = value.lower()
    elif value.upper() in mapping:
        value = value.upper()
    return mapping.get(value,'Others')
