from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from django.db.models.query import QuerySet
from console.common.mixins import ListPartialMixin, DetailPartialMixin, UpdatableDetailPartialMixin, AddPartialMixin
from partner.api.core.mixins import VendorViewMixin, VendorHierarchyViewMixin
from order.api.core.mixins import OrderItemViewMixin
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


class OrderMixin:
    def get_queryset(self):
        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.filter(partner__id=self.kwargs['vendor_id'])
        return queryset


class OrderListPartialMixin(OrderMixin, ListPartialMixin):
    pass


class OrderDetailPartialMixin(OrderMixin, DetailPartialMixin):
    pass


class NewOrdersListPartial(OrderListPartialMixin, OrderItemViewMixin, ListAPIView):

    template_name = partial_template_name = 'console/partner/partials/neworders-list-partial.html'

    def get_queryset(self):
        return super(NewOrdersListPartial, self).get_queryset().filter(order__status__in=[1,2])


class NewOrdersDetailPartial(OrderDetailPartialMixin, OrderItemViewMixin, RetrieveAPIView):
    template_name = partial_template_name = 'console/partner/partials/neworders-detail-partial.html'
    success_list_redirect = 'console:partner:pages:neworders-list'
    success_detail_redirect = 'console:partner:pages:neworders-detail'


class ClosedOrdersListPartial(OrderListPartialMixin, OrderItemViewMixin, ListAPIView):

    template_name = partial_template_name = 'console/partner/partials/closedorders-list-partial.html'

    def get_queryset(self):
        return super(NewOrdersListPartial, self).get_queryset().filter(order__status=3)


class ClosedOrdersDetailPartial(OrderDetailPartialMixin, OrderItemViewMixin, RetrieveAPIView):
    template_name = partial_template_name = 'console/partner/partials/closedorders-detail-partial.html'
    success_list_redirect = 'console:partner:pages:closedorders-list'
    success_detail_redirect = 'console:partner:pages:closedorders-detail'


class HeldOrdersListPartial(OrderListPartialMixin, OrderItemViewMixin, ListAPIView):
    template_name = partial_template_name = 'console/partner/partials/heldorders-list-partial.html'

    def get_queryset(self):
        return super(NewOrdersListPartial, self).get_queryset().filter(order__status=2)


class HeldOrdersDetailPartial(OrderDetailPartialMixin, OrderItemViewMixin, RetrieveAPIView):
    template_name = partial_template_name = 'console/partner/partials/heldorders-detail-partial.html'
    success_list_redirect = 'console:partner:pages:heldorders-list'
    success_detail_redirect = 'console:partner:pages:heldorders-detail'
