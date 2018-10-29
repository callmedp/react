from rest_framework.generics import ListAPIView
from shop.models import Product
from .serializers import ProductListSerializerForAuditHistory
from rest_framework.authentication import SessionAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from shared.rest_addons.mixins import FieldFilterMixin


class ProductListView(FieldFilterMixin, ListAPIView):
    serializer_class = ProductListSerializerForAuditHistory
    authentication_classes = (SessionAuthentication,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('vendor',)

    def get_queryset(self):
        """
        Return product List only if any of filter fields is present in
        query params.
        """
        for fltr in self.filter_fields:
            val = self.request.GET.get(fltr, None)
            if val is not None:
                return Product.objects.all()
        return Product.objects.none()
