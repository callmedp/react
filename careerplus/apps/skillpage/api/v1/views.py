from rest_framework.generics import ListAPIView
from shared.rest_addons.pagination import LearningCustomPagination
from .serializers import LoadMoreSerializerSolr
from django.conf import settings
from core.library.haystack.query import SQS
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser, )
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from shared.rest_addons.mixins import FieldFilterMixin
from django_filters.rest_framework import DjangoFilterBackend


class LoadMoreApiView(FieldFilterMixin, ListAPIView):
    serializer_class = LoadMoreSerializerSolr
    pagination_class = LearningCustomPagination
    permission_classes = []
    authentication_classes = []

    def get_queryset(self, *args, **kwargs):
        pCtg = self.request.query_params.get('pCtg', None)
        pTF = self.request.query_params.get('pTF', 16)
        pTF_include = self.request.query_params.get('pTF_include')

        if pCtg is None:
            return []

        if pTF_include == 'true':
            return SQS().exclude(id__in=settings.EXCLUDE_SEARCH_PRODUCTS).filter(pCtg=pCtg, pTF=pTF)    

        return SQS().exclude(id__in=settings.EXCLUDE_SEARCH_PRODUCTS).filter(pCtg=pCtg).exclude(pTF=pTF)