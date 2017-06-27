from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from partner.api.core.mixins import VendorViewMixin, VendorHierarchyViewMixin


class VendorViewSet(VendorViewMixin, ModelViewSet):
    """
        CRUD Viewset for `Vendor` model.
    """


class VendorHierarchyViewSet(VendorHierarchyViewMixin, ReadOnlyModelViewSet):
    """
        CRUD Viewset for `VendorHierarchy` model.
    """
