#python imports

# django imports
from django.conf.urls import url, include

# local imports
from .views import (OrderItemViewSet,OrderItemsListView,OrderUpdateView,
					OrderItemOperationApiView,MessageCommunicationListApiView,LTVReportView)
# inter app imports

# 3rd party imports
from rest_framework import routers


router = routers.SimpleRouter()

router.register(r'orderitem', OrderItemViewSet)

urlpatterns = router.urls

urlpatterns = [
    url(r'^orderitem/$', OrderItemViewSet),
    url(r'^order/(?P<pk>\d+)/items/$', OrderItemsListView.as_view()),
    url(r'^order/(?P<pk>\d+)/update/$', OrderUpdateView.as_view()),
	url(r'^order/order-item-operation/(?P<oi_id>\d+)/$',
		OrderItemOperationApiView.as_view(),
		name='orderitemoperations'),
	url(r'^order/order-item/(?P<oi_id>\d+)/message/$',
		MessageCommunicationListApiView.as_view(),
		name='message-communications'),

    url(r'^ltv-report/(?P<year>\d+)/(?P<month>\d+)/$', LTVReportView.as_view()),
]