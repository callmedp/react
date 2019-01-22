# python imports

# django imports
from django.http import Http404

# local imports
from console.api.core.serializers import ProductSkillSerializer

# inter app imports
from shop.models import ProductSkill

# third party imports
from rest_framework.generics import ListCreateAPIView, CreateAPIView, ListAPIView


class ProductSkillAddView(CreateAPIView):
    queryset = ProductSkill.objects.all()
    serializer_class = ProductSkillSerializer

    def get(self, request, format=None):
        raise Http404('No get Request')

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(ProductSkillAddView, self).get_serializer(*args, **kwargs)
