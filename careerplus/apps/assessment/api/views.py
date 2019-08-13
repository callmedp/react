from rest_framework.generics import ListAPIView
from shop.api.v1.serializers import CategorySerializer
from shop.models import Category
from shared.rest_addons.pagination import LearningCustomPagination
from shared.rest_addons.mixins import FieldFilterMixin
from assessment.models import Test
from assessment.serializers import TestSerializer

from rest_framework.response import Response


class CategoryApiView(FieldFilterMixin,ListAPIView):
    """
    Field params -

    fl - Takes

    Include Params -

    include_pid - Includes data of all parent categories

    Filter params -

    only_test_level3category =true - will show all category level3 with test
    or
    only_test_level2category =true - will show all the category level2  with test

    test_category -  will show the parent category for that particular category
    works for only getting level 3 categorys


    type_flow -  will filter out the category.Accepts comma separated values

    """
    permission_classes = []
    authentication_classes = []
    pagination_class = LearningCustomPagination
    serializer_class = CategorySerializer

    def get_level3_test_category(self,val=False):
        queryset = Category.objects.all()
        filter_dict = {}
        if self.request.query_params.get('only_test_level3category') or val:
            filter_dict.update({'category__categoryproducts__type_flow': 16,'category__active': True})

        if self.request.query_params.get('test_category_id'):
            filter_dict.update({'category__related_to':self.request.query_params.get('test_category_id')})

        level3_ids = list(set(Test.objects.filter(**filter_dict).\
                             values_list('category__id',flat=True)))

        return queryset.filter(id__in=level3_ids)

    def get_level2_test_category(self):
        filter_dict = {}
        queryset = self.get_level3_test_category(val=True)
        filter_dict.update({'from_category__active': True,'from_category__is_main_parent': True})

        queryset = list(set(queryset.filter(**filter_dict).\
                            values_list('from_category__related_to__id', flat=True)))
        return Category.objects.filter(id__in=queryset, active=True)

    def get_queryset(self):
        queryset = None
        filter_dict = {}
        if self.request.query_params.get('only_test_level3category'):
            queryset = self.get_level3_test_category()
        elif self.request.query_params.get('only_test_level2category'):
            queryset = self.get_level2_test_category()
        else:
            queryset = Category.objects.all()
        if self.request.query_params.get('type_flow'):
            type_flow = self.request.query_params.get('type_flow').split(',')
            filter_dict.update({'type_flow__in': type_flow})
        if self.request.query_params.get('only_test_level2category'):
            pass
        return queryset


class TestApiView(FieldFilterMixin, ListAPIView):
    """
    Filter params:
                active = True  => To show all active tests only
                category_id = 1  ==> To show all the test for particular category

                test_for_products = True ==> To show all tests with a paid tests product


    """
    permission_classes = []
    authentication_classes = []
    pagination_class = LearningCustomPagination
    serializer_class = TestSerializer
    queryset = Test.objects.all()


    def get_category_test(self):
        queryset = self.queryset
        filter_dict = {}
        if self.request.query_params.get('test_for_products'):
            filter_dict = {'category__categoryproducts__type_flow':16}
        if self.request.query_params.get('category_id'):
            filter_dict.update({'category__id': self.request.query_params.get('category_id')})
        if self.request.query_params.get('active'):
            filter_dict.update({'is_active': True})
        return queryset.filter(**filter_dict)

    def get_queryset(self):
        return self.get_category_test()
