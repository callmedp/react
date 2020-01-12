#python imports

# django imports
from django.conf.urls import url

# local imports
from .views import (OrderItemViewSet,OrderItemsListView,OrderUpdateView,
							OrderItemUpdateView,OrderItemOperationApiView,
							MessageCommunicationListApiView,LTVReportView)
# inter app imports

# 3rd party imports
from rest_framework import routers


router = routers.SimpleRouter()

# router.register(r'orderitem', OrderItemViewSet)

urlpatterns = router.urls
app_name = "order"
urlpatterns = [
    url(r'^orderitem/$', OrderItemViewSet),
    url(r'^(?P<pk>\d+)/items/$', OrderItemsListView.as_view()),
    url(r'^(?P<pk>\d+)/update/$', OrderUpdateView.as_view()),
	url(r'^orderitem/(?P<pk>\d+)/update/$',OrderItemUpdateView.as_view()),
	url(r'^order-item-operation/(?P<oi_id>\d+)/$',
		OrderItemOperationApiView.as_view(),
		name='orderitemoperations'),
	url(r'^order-item/(?P<oi_id>\d+)/message/$',
		MessageCommunicationListApiView.as_view(),
		name='message-communications'),
    url(r'^ltv-report/(?P<year>\d+)/(?P<month>\d+)/$', LTVReportView.as_view()),
]