# Python Core Import
import logging

# Django-Core Import
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.http import Http404

# Inter-App Import
from core.common import APIResponse
from shop.views import ProductInformationMixin
from shop.models import (Product, Skill)
from .serializers import (
    ProductDetailSerializer)

# DRF Import
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny


class ProductDetailAPI(ProductInformationMixin, APIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductDetailSerializer

    def get_object(self, pid):
        try:
            return Product.objects.get(pk=pid)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        pid = self.request.GET.get('pid')
        slug = self.request.GET.get('slug')
        user = self.request.user

        product = self.get_object(pid)

        serializer_obj = ProductDetailSerializer(product)

        return APIResponse(data=serializer_obj.data)