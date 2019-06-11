from rest_framework.generics import ListAPIView
from shop.api.v1.serializers import CategorySerializer
from shop.models import Category
from shared.rest_addons.pagination import Learning_custom_pagination
from shared.rest_addons.mixins import FieldFilterMixin
from rest_framework.response import Response


class CategoryApiView(FieldFilterMixin,ListAPIView):
    permission_classes = []
    authentication_classes = []
    pagination_class = Learning_custom_pagination
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all()
        filter_dict = {}
        if self.request.GET.get('tl') and self.request.GET.get('tl').isdigit():
            filter_dict.update({'type_level': self.request.GET.get('tl')})
        return queryset.filter(**filter_dict)



