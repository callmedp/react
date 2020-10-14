from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.query import QuerySet
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.utils.safestring import mark_safe
from django.template import Library

register = Library()

@register.filter
def jsonify(obj):
    if isinstance(obj, str):
        try:
            return json.loads(obj)
        except:
            return obj
    return obj
