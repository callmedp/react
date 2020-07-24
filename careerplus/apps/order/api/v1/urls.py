# python imports

# django imports
# from django.conf.urls import url
from django.urls import re_path

# local imports
from .views import (OrderItemViewSet, OrderItemsListView, OrderUpdateView,
                    OrderItemUpdateView, OrderItemOperationApiView,
                    MessageCommunicationListApiView, LTVReportView, OrderItemPatchView,
                    DirectOrderCreateApiView)
# inter app imports

# 3rd party imports
from rest_framework import routers


router = routers.SimpleRouter()

# router.register(r'orderitem', OrderItemViewSet)

urlpatterns = router.urls
app_name = "order"
urlpatterns = [
    re_path(r'^orderitem/$', OrderItemViewSet),
    re_path(r'^(?P<pk>\d+)/items/$', OrderItemsListView.as_view()),
    re_path(r'^(?P<pk>\d+)/update/$', OrderUpdateView.as_view()),
    re_path(r'^orderitem/modify/$', OrderItemPatchView.as_view()),
    re_path(r'^orderitem/(?P<pk>\d+)/update/$', OrderItemUpdateView.as_view()),
    re_path(r'^order-item-operation/(?P<oi_id>\d+)/$',
            OrderItemOperationApiView.as_view(),
            name='orderitemoperations'),
    re_path(r'^order-item/(?P<oi_id>\d+)/message/$',
            MessageCommunicationListApiView.as_view(),
            name='message-communications'),
    re_path(r'^ltv-report/(?P<year>\d+)/(?P<month>\d+)/$',
            LTVReportView.as_view()),
    re_path(r'^direct-order/$', DirectOrderCreateApiView.as_view())
]
