from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^vendor/$', views.VendorListPartial.as_view(), name='vendor-list-partial'),
	url(r'^vendorhierarchy/$', views.VendorHierarchyListPartial.as_view(), name='vendorhierarchy-list-partial'),
	url(r'^vendor/add/$', views.VendorAddPartial.as_view(), name='vendor-add-partial'),
	url(r'^vendorhierarchy/add/$', views.VendorHierarchyAddPartial.as_view(), name='vendorhierarchy-add-partial'),
	url(r'^vendor/(?P<pk>\d+)/$', views.VendorDetailPartial.as_view(), name='vendor-detail-partial'),
	url(r'^vendorhierarchy/(?P<pk>\d+)/$', views.VendorHierarchyDetailPartial.as_view(), name='vendorhierarchy-detail-partial'),
	url(r'^vendor/(?P<vendor_id>\d+)/neworders/$', views.NewOrdersListPartial.as_view(), name='neworders-list-partial'),
	url(r'^vendor/(?P<vendor_id>\d+)/closedorders/$', views.ClosedOrdersListPartial.as_view(), name='closedorders-list-partial'),
	url(r'^vendor/(?P<vendor_id>\d+)/heldorders/$', views.HeldOrdersListPartial.as_view(), name='heldorders-list-partial'),
	url(r'^vendor/(?P<vendor_id>\d+)/neworders/(?P<pk>\d+)/$', views.NewOrdersDetailPartial.as_view(), name='neworders-detail-partial'),
	url(r'^vendor/(?P<vendor_id>\d+)/closedorders/(?P<pk>\d+)/$', views.ClosedOrdersDetailPartial.as_view(), name='closedorders-detail-partial'),
	url(r'^vendor/(?P<vendor_id>\d+)/heldorders/(?P<pk>\d+)/$', views.HeldOrdersDetailPartial.as_view(), name='heldorders-detail-partial'),
	
]
