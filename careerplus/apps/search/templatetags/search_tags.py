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

register = template.Library()

@register.filter
def get_choice_display(value, choice):
    """
    Return user displayable value of against a lookup id. Mainly used while
    listing facets but can be used elsewhere
    """
    try:
        mapping = dict(getattr(choices, choice))
        if value not in mapping:
            if value.isdigit():
                value = int(value)
            elif value.lower() in mapping:
                value = value.lower()
            elif value.upper() in mapping:
                value = value.upper()
        return mapping[value]
    except:
        return 'Others'
