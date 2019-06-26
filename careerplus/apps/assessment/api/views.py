from rest_framework.generics import ListAPIView
from shop.api.v1.serializers import CategorySerializer
from shop.models import Category
from shared.rest_addons.pagination import LearningCustomPagination
from shared.rest_addons.mixins import FieldFilterMixin
from assessment.models import Test
from assessment.serializers import TestSerializer

from rest_framework.response import Response


class CategoryApiView(FieldFilterMixin,ListAPIView):
    permission_classes = []
    authentication_classes = []
    pagination_class = LearningCustomPagination
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all()
        category_ids = Test.objects.filter(category__categoryproducts__type_flow=16, category__active=True) \
            .values_list('category__id', flat=True)

        if self.request.GET.get('level3assessments'):
            return queryset.filter(id__in=category_ids)

        cat_ids = list(set(Category.objects.filter(id__in=category_ids, from_category__active=True,
                                          from_category__is_main_parent=True).\
                           values_list('from_category__related_to__id', flat=True)))
        if not cat_ids:
            return queryset.none()
        queryset = queryset.filter(id__in=cat_ids)
        filter_dict = {}
        if self.request.GET.get('tl') and self.request.GET.get('tl').isdigit():
            filter_dict.update({'type_level': self.request.GET.get('tl')})
        return queryset.filter(**filter_dict)


class TestApiView(FieldFilterMixin,ListAPIView):
    permission_classes = []
    authentication_classes = []
    pagination_class = LearningCustomPagination
    serializer_class = TestSerializer

    def get_queryset(self):
        test = Test.objects.exclude(category__categoryproducts__type_flow=16)
        return test



