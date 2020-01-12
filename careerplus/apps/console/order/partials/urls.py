from django.conf.urls import url
from . import views
app_name = 'console'
urlpatterns = [
	url(r'^neworders/$', views.NewOrdersListPartial.as_view(), name='neworders-list-partial'),
	url(r'^closedorders/$', views.ClosedOrdersListPartial.as_view(), name='closedorders-list-partial'),
	url(r'^heldorders/$', views.HeldOrdersListPartial.as_view(), name='heldorders-list-partial'),
	url(r'^neworders/(?P<pk>\d+)/$', views.NewOrdersDetailPartial.as_view(), name='neworders-detail-partial'),
	url(r'^closedorders/(?P<pk>\d+)/$', views.ClosedOrdersDetailPartial.as_view(), name='closedorders-detail-partial'),
	url(r'^heldorders/(?P<pk>\d+)/$', views.HeldOrdersDetailPartial.as_view(), name='heldorders-detail-partial'),
	url(r'^neworders/(?P<pk>\d+)/change/$', views.NewOrdersUpdatableDetailPartial.as_view(), name='neworders-detail-change-partial'),
	url(r'^closedorders/(?P<pk>\d+)/change/$', views.ClosedOrdersUpdatableDetailPartial.as_view(), name='closedorders-detail-change-partial'),
	url(r'^heldorders/(?P<pk>\d+)/change/$', views.HeldOrdersUpdatableDetailPartial.as_view(), name='heldorders-detail-change-partial'),
	
]
