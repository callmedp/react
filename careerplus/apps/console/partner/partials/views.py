from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from console.common.mixins import ListPartialMixin, UpdatableDetailPartialMixin, AddPartialMixin
from partner.api.core.mixins import VendorViewMixin, VendorHierarchyViewMixin
from partner.api.core.serializers import VendorSerializer, VendorHierarchySerializer  
from partner.models import Vendor, VendorHierarchy
 
class VendorListPartial(ListPartialMixin, VendorViewMixin, ListAPIView):

    template_name = partial_template_name = 'console/partner/partials/vendor-list-partial.html'


class VendorHierarchyListPartial(ListPartialMixin, VendorHierarchyViewMixin, ListAPIView):

    template_name = partial_template_name = 'console/partner/partials/vendorhierarchy-list-partial.html'


class VendorDetailPartial(UpdatableDetailPartialMixin, VendorViewMixin, RetrieveUpdateAPIView):
    template_name = partial_template_name = 'console/partner/partials/vendor-detail-partial.html'
    success_list_redirect = 'console:partner:pages:vendor-list'
    success_detail_redirect = 'console:partner:pages:vendor-detail'


class VendorHierarchyDetailPartial(UpdatableDetailPartialMixin, VendorHierarchyViewMixin, RetrieveUpdateAPIView):
    template_name = partial_template_name = 'console/partner/partials/vendorhierarchy-detail-partial.html'
    success_list_redirect = 'console:partner:pages:vendorhierarchy-list'
    success_detail_redirect = 'console:partner:pages:vendorhierarchy-detail'


class VendorAddPartial(AddPartialMixin, VendorViewMixin, CreateAPIView):
    template_name = partial_template_name = 'console/partner/partials/vendor-add-partial.html'
    success_list_redirect = 'console:partner:pages:vendor-list'
    success_detail_redirect = 'console:partner:pages:vendor-detail'


class VendorHierarchyAddPartial(AddPartialMixin, VendorHierarchyViewMixin, CreateAPIView):
    template_name = partial_template_name = 'console/partner/partials/vendorhierarchy-add-partial.html'
    success_list_redirect = 'console:partner:pages:vendorhierarchy-list'
    success_detail_redirect = 'console:partner:pages:vendorhierarchy-detail'
