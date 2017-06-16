from rest_framework.viewsets import ReadOnlyModelViewSet

from order.api.core.mixins import OrderItemViewMixin


class OrderItemViewSet(OrderItemViewMixin, ReadOnlyModelViewSet):
    """
        CRUD Viewset for `OrderItem` model.
    """
