from rest_framework.generics import ListAPIView
from shared.rest_addons.pagination import LearningCustomPagination
from .serializers import CertificationLoadMoreSerializerSolr
from django.conf import settings
from core.library.haystack.query import SQS
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser, )
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from shared.rest_addons.mixins import FieldFilterMixin
from django_filters.rest_framework import DjangoFilterBackend


class CertificationLoadMoreApiView(FieldFilterMixin, ListAPIView):
    serializer_class = CertificationLoadMoreSerializerSolr
    pagination_class = LearningCustomPagination
    permission_classes = []
    authentication_classes = []

    def get_queryset(self, *args, **kwargs):
        pCtg = self.request.query_params.get('pCtg', None)
        pTF = self.request.query_params.get('pTF', 16)
        pTF_include = self.request.query_params.get('pTF_include')

        if pCtg is not None:
            if pTF_include == 'true':
                certifications = SQS().exclude(id__in=settings.EXCLUDE_SEARCH_PRODUCTS).filter(pCtg=pCtg, pTF=pTF)    
            else :
                certifications = SQS().exclude(id__in=settings.EXCLUDE_SEARCH_PRODUCTS).filter(pCtg=pCtg).exclude(pTF=pTF)

        return certifications