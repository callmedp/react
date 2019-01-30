# python imports

# django imports

# local imports
from console.api.core.serializers import (ProductSkillSerializer, SkillSerializer, ProductSerializer)

# inter app imports
from shop.models import (ProductSkill, Product, Skill)

# third party imports
from rest_framework.generics import (ListCreateAPIView, CreateAPIView, ListAPIView, RetrieveUpdateAPIView, )



class ProductSkillAddView(ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ProductSkillSerializer

    def get_queryset(self):
        product_id = self.request.GET.get('product_id')
        return ProductSkill.objects.all().filter(product_id=product_id).select_related('skill')

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(ProductSkillAddView, self).get_serializer(*args, **kwargs)


class ProductSkillUpdateView(RetrieveUpdateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ProductSkillSerializer

    def get_queryset(self):
        product_skill_id = int(self.kwargs.get('pk'))
        return ProductSkill.objects.filter(id=product_skill_id)


class ProductListView(ListAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.selected.all().select_related('product_class')


class SkillListView(ListAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = Skill.objects.only('id', 'name', ).filter(active=True)
    serializer_class = SkillSerializer
