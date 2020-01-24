# from django.conf.urls import url
from django.urls import re_path
from .import views
from console.order.pages import views as order_views

app_name = 'console'
urlpatterns = [
	re_path(r'^vendor/$', views.VendorListView.as_view(), name='vendor-list'),
	re_path(r'^vendorhierarchy/$', views.VendorHierarchyListView.as_view(), name='vendorhierarchy-list'),
	re_path(r'^vendor/add/$', views.VendorAddView.as_view(), name='vendor-add'),
	re_path(r'^vendorhierarchy/add/$', views.VendorHierarchyAddView.as_view(), name='vendorhierarchy-add'),
	re_path(r'^vendor/(?P<pk>[\d]+)/$', views.VendorDetailView.as_view(), name='vendor-detail'),
	re_path(r'^vendorhierarchy/(?P<pk>\d+)/$', views.VendorHierarchyDetailView.as_view(), name='vendorhierarchy-detail'),
	re_path(r'^vendor/(?P<vendor_id>([\d]+))/neworders/$', order_views.NewOrdersListView.as_view(), name='neworders-list'),
	re_path(r'^vendor/(?P<vendor_id>\d+)/closedorders/$', order_views.ClosedOrdersListView.as_view(), name='closedorders-list'),
	re_path(r'^vendor/(?P<vendor_id>\d+)/heldorders/$', order_views.HeldOrdersListView.as_view(), name='heldorders-list'),
	re_path(r'^vendor/(?P<vendor_id>\d+)/neworders/(?P<pk>\d+)/$', order_views.NewOrdersDetailView.as_view(), name='neworders-detail'),
	re_path(r'^vendor/(?P<vendor_id>\d+)/closedorders/(?P<pk>\d+)/$', order_views.ClosedOrdersDetailView.as_view(), name='closedorders-detail'),
	re_path(r'^vendor/(?P<vendor_id>\d+)/heldorders/(?P<pk>\d+)/$', order_views.HeldOrdersDetailView.as_view(), name='heldorders-detail'),
]
