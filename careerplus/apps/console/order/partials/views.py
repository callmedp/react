from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser
from django.db.models.query import QuerySet
from console.common.mixins import ListPartialMixin, DetailPartialMixin, UpdatableDetailPartialMixin, AddPartialMixin
from order.api.core.mixins import OrderItemViewMixin
from partner.api.core.permissions import IsAdminOrEmployeeOfVendor
 
class OrderMixin:
    permission_classes = (IsAdminOrEmployeeOfVendor, )
    def get_queryset(self):
        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet) and 'vendor_id' in self.kwargs:
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.filter(partner__id=self.kwargs['vendor_id'])
        if hasattr(self.request.user, 'vendor_set') and self.request.user.vendor_set.count():
            queryset = queryset.filter(partner__id=self.request.user.vendor_set.all()[0].id)
        return queryset


class OrderListPartialMixin(OrderMixin, ListPartialMixin):
    pass


class OrderDetailPartialMixin(OrderMixin, DetailPartialMixin):
    pass


class OrderUpdatableDetailPartialMixin(OrderMixin, UpdatableDetailPartialMixin):
    permission_classes = (IsAdminUser, )


class NewOrdersListPartial(OrderListPartialMixin, OrderItemViewMixin, ListAPIView):

    template_name = partial_template_name = 'console/order/partials/neworders-list-partial.html'

    def get_queryset(self):
        return super(NewOrdersListPartial, self).get_queryset().filter(oi_status__in=range(0,9)).order_by('-date_placed')


class NewOrdersDetailPartial(OrderDetailPartialMixin, OrderItemViewMixin, RetrieveAPIView):
    template_name = partial_template_name = 'console/order/partials/neworders-detail-partial.html'
    success_list_redirect = 'console:order:pages:neworders-list'
    success_detail_redirect = 'console:order:pages:neworders-detail'


class NewOrdersUpdatableDetailPartial(OrderUpdatableDetailPartialMixin, OrderItemViewMixin, RetrieveUpdateAPIView):
    template_name = partial_template_name = 'console/order/partials/neworders-detail-change-partial.html'
    success_list_redirect = 'console:order:pages:neworders-list'
    success_detail_redirect = 'console:order:pages:neworders-detail'


class ClosedOrdersListPartial(OrderListPartialMixin, OrderItemViewMixin, ListAPIView):

    template_name = partial_template_name = 'console/order/partials/closedorders-list-partial.html'

    def get_queryset(self):
        return super(ClosedOrdersListPartial, self).get_queryset().filter(oi_status=9).order_by('-date_placed')


class ClosedOrdersDetailPartial(OrderDetailPartialMixin, OrderItemViewMixin, RetrieveAPIView):
    template_name = partial_template_name = 'console/order/partials/closedorders-detail-partial.html'
    success_list_redirect = 'console:order:pages:closedorders-list'
    success_detail_redirect = 'console:order:pages:closedorders-detail'


class ClosedOrdersUpdatableDetailPartial(OrderUpdatableDetailPartialMixin, OrderItemViewMixin, RetrieveUpdateAPIView):
    template_name = partial_template_name = 'console/order/partials/closedorders-detail-change-partial.html'
    success_list_redirect = 'console:order:pages:closedorders-list'
    success_detail_redirect = 'console:order:pages:closedorders-detail'


class HeldOrdersListPartial(OrderListPartialMixin, OrderItemViewMixin, ListAPIView):
    template_name = partial_template_name = 'console/order/partials/heldorders-list-partial.html'

    def get_queryset(self):
        return super(HeldOrdersListPartial, self).get_queryset().filter(oi_status=10).order_by('-date_placed')


class HeldOrdersDetailPartial(OrderDetailPartialMixin, OrderItemViewMixin, RetrieveAPIView):
    template_name = partial_template_name = 'console/order/partials/heldorders-detail-partial.html'
    success_list_redirect = 'console:order:pages:heldorders-list'
    success_detail_redirect = 'console:order:pages:heldorders-detail'


class HeldOrdersUpdatableDetailPartial(OrderUpdatableDetailPartialMixin, OrderItemViewMixin, RetrieveUpdateAPIView):
    template_name = partial_template_name = 'console/order/partials/heldorders-detail-change-partial.html'
    success_list_redirect = 'console:order:pages:heldorders-list'
    success_detail_redirect = 'console:order:pages:heldorders-detail'
 