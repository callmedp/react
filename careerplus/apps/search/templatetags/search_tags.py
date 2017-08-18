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
        return dict(getattr(choices, choice))[int(value) if value.isdigit() else value]
    except:
        return 'Others'
