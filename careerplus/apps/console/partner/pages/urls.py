from django.conf.urls import url
from .import views

urlpatterns = [
	url(r'^vendor/$', views.VendorListView.as_view(), name='vendor-list'),
	url(r'^vendorhierarchy/$', views.VendorHierarchyListView.as_view(), name='vendorhierarchy-list'),
	url(r'^vendor/add/$', views.VendorAddView.as_view(), name='vendor-add'),
	url(r'^vendorhierarchy/add/$', views.VendorHierarchyAddView.as_view(), name='vendorhierarchy-add'),
	url(r'^vendor/(?P<pk>[\d]+)/$', views.VendorDetailView.as_view(), name='vendor-detail'),
	url(r'^vendorhierarchy/(?P<pk>\d+)/$', views.VendorHierarchyDetailView.as_view(), name='vendorhierarchy-detail'),
	url(r'^vendor/(?P<vendor_id>([\d]+))/neworders/$', views.NewOrdersListView.as_view(), name='neworders-list'),
	url(r'^vendor/(?P<vendor_id>\d+)/closedorders/$', views.ClosedOrdersListView.as_view(), name='closedorders-list'),
	url(r'^vendor/(?P<vendor_id>\d+)/heldorders/$', views.HeldOrdersListView.as_view(), name='heldorders-list'),
	url(r'^vendor/(?P<vendor_id>\d+)/neworders/(?P<pk>\d+)/$', views.NewOrdersDetailView.as_view(), name='neworders-detail'),
	url(r'^vendor/(?P<vendor_id>\d+)/closedorders/(?P<pk>\d+)/$', views.ClosedOrdersDetailView.as_view(), name='closedorders-detail'),
	url(r'^vendor/(?P<vendor_id>\d+)/heldorders/(?P<pk>\d+)/$', views.HeldOrdersDetailView.as_view(), name='heldorders-detail'),
]
