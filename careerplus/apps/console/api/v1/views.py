# python imports

# django imports
from django.conf import settings

# local imports
from console.api.core.serializers import (ProductSkillSerializer, SkillSerializer, ProductSerializer)

# inter app imports
from shop.models import (ProductSkill, Product, Skill)

# third party imports
from rest_framework.generics import (ListCreateAPIView, CreateAPIView, ListAPIView, RetrieveUpdateAPIView, )
from rest_framework.pagination import PageNumberPagination


class StandardResultSetPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 10000


class ProductSkillAddView(ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ProductSkillSerializer
    pagination_class = None

    def get_queryset(self):
        product_id = self.request.GET.get('product_id')
        active = self.request.GET.get('active')
        if active == 'True':
            return ProductSkill.objects.all().filter(product_id=product_id, active=True).select_related('skill')
        else:
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
    pagination_class = StandardResultSetPagination

    def get_queryset(self):

        courses = self.request.GET.get('courses')
        search_text = self.request.GET.get('search')
        if courses == 'True' and search_text is not None:
            return Product.selected.all().select_related('product_class').filter(name__icontains=search_text,
                                                                                 product_class__slug__in=settings.COURSE_SLUG)
        elif courses == 'True':
            return Product.selected.all().select_related('product_class').filter(produt_class__slug__in=settings.COURSE_SLUG)
        if search_text is not None:
            return Product.selected.all().select_related('product_class').filter(name__icontains=search_text)
        else:
            return Product.selected.all().select_related('product_class')


class SkillListView(ListAPIView):
    authentication_classes = ()
    permission_classes = ()
    pagination_class = StandardResultSetPagination
    serializer_class = SkillSerializer

    def get_queryset(self):

        product_id = self.request.GET.get('exel_prd_skill')
        search_text = self.request.GET.get('search')
        product_skill_list = []
        query_value_list = []

        if product_id:
            product_skill_list = ProductSkill.objects.all().filter(product_id=product_id)
            query_value_list = product_skill_list.values_list('skill_id', flat=True)

        if product_id is not None and search_text is not None:
            return Skill.objects.only('id', 'name', ).filter(active=True, name__icontains=search_text).exclude(
                id__in=query_value_list)

        elif product_id is not None:
            return Skill.objects.only('id', 'name', ).filter(active=True).exclude(id__in=query_value_list)

        elif search_text is not None:
            return Skill.objects.only('id', 'name', ).filter(active=True, name__icontains=search_text)

        else:
            return Skill.objects.only('id', 'name', ).filter(active=True)
