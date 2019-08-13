from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from order.api.core.mixins import OrderItemViewMixin
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from order.models import Order


class OrderItemViewSet(OrderItemViewMixin, ModelViewSet):
    """
        CRUD Viewset for `OrderItem` model.
    """


