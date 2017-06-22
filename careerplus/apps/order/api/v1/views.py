from rest_framework.viewsets import ModelViewSet

from order.api.core.mixins import OrderItemViewMixin


class OrderItemViewSet(OrderItemViewMixin, ModelViewSet):
    """
        CRUD Viewset for `OrderItem` model.
    """
