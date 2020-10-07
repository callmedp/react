
# third party import
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
# inter-app import
from partner.api.core.mixins import VendorViewMixin, VendorHierarchyViewMixin
from .serializers import VendorListSerializer
from partner.models import Vendor
from shared.rest_addons.mixins import FieldFilterMixin

class VendorViewSet(VendorViewMixin, ModelViewSet):
    """
        CRUD Viewset for `Vendor` model.
    """


class VendorHierarchyViewSet(VendorHierarchyViewMixin, ReadOnlyModelViewSet):
    """
        CRUD Viewset for `VendorHierarchy` model.
    """



class VendorListApiView(FieldFilterMixin, ListAPIView):
    """
    Get Vendor List Api End point
    """
    queryset = Vendor.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    serializer_class = VendorListSerializer
