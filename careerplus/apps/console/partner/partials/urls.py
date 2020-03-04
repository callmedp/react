# from django.conf.urls import url
from django.urls import re_path
from . import views
from console.order.partials import views as order_views
app_name = "console"
urlpatterns = [
	re_path(r'^vendor/$', views.VendorListPartial.as_view(), name='vendor-list-partial'),
	re_path(r'^vendorhierarchy/$', views.VendorHierarchyListPartial.as_view(), name='vendorhierarchy-list-partial'),
	re_path(r'^vendor/add/$', views.VendorAddPartial.as_view(), name='vendor-add-partial'),
	re_path(r'^vendorhierarchy/add/$', views.VendorHierarchyAddPartial.as_view(), name='vendorhierarchy-add-partial'),
	re_path(r'^vendor/(?P<pk>\d+)/$', views.VendorDetailPartial.as_view(), name='vendor-detail-partial'),
	re_path(r'^vendorhierarchy/(?P<pk>\d+)/$', views.VendorHierarchyDetailPartial.as_view(), name='vendorhierarchy-detail-partial'),
	re_path(r'^vendor/(?P<vendor_id>\d+)/neworders/$', order_views.NewOrdersListPartial.as_view(), name='neworders-list-partial'),
	re_path(r'^vendor/(?P<vendor_id>\d+)/closedorders/$', order_views.ClosedOrdersListPartial.as_view(), name='closedorders-list-partial'),
	re_path(r'^vendor/(?P<vendor_id>\d+)/heldorders/$', order_views.HeldOrdersListPartial.as_view(), name='heldorders-list-partial'),
	re_path(r'^vendor/(?P<vendor_id>\d+)/neworders/(?P<pk>\d+)/$', order_views.NewOrdersDetailPartial.as_view(), name='neworders-detail-partial'),
	re_path(r'^vendor/(?P<vendor_id>\d+)/closedorders/(?P<pk>\d+)/$', order_views.ClosedOrdersDetailPartial.as_view(), name='closedorders-detail-partial'),
	re_path(r'^vendor/(?P<vendor_id>\d+)/heldorders/(?P<pk>\d+)/$', order_views.HeldOrdersDetailPartial.as_view(), name='heldorders-detail-partial'),
	
]
