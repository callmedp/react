from django.conf.urls import url
from .import views

urlpatterns = [
	url(r'^neworders/$', views.NewOrdersListView.as_view(), name='neworders-list'),
	url(r'^closedorders/$', views.ClosedOrdersListView.as_view(), name='closedorders-list'),
	url(r'^heldorders/$', views.HeldOrdersListView.as_view(), name='heldorders-list'),
	url(r'^neworders/(?P<pk>\d+)/$', views.NewOrdersDetailView.as_view(), name='neworders-detail'),
	url(r'^closedorders/(?P<pk>\d+)/$', views.ClosedOrdersDetailView.as_view(), name='closedorders-detail'),
	url(r'^heldorders/(?P<pk>\d+)/$', views.HeldOrdersDetailView.as_view(), name='heldorders-detail'),
	url(r'^neworders/(?P<pk>\d+)/change/$', views.NewOrdersUpdatableDetailView.as_view(), name='neworders-detail-change'),
	url(r'^closedorders/(?P<pk>\d+)/change/$', views.ClosedOrdersUpdatableDetailView.as_view(), name='closedorders-detail-change'),
	url(r'^heldorders/(?P<pk>\d+)/change/$', views.HeldOrdersUpdatableDetailView.as_view(), name='heldorders-detail-change'),
]
