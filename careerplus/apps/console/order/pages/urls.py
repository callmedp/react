# from django.conf.urls import url
from django.urls import re_path

from .import views

app_name = 'console'

urlpatterns = [
    re_path(r'^neworders/$', views.NewOrdersListView.as_view(), name='neworders-list'),
    re_path(r'^closedorders/$', views.ClosedOrdersListView.as_view(), name='closedorders-list'),
    re_path(r'^heldorders/$', views.HeldOrdersListView.as_view(), name='heldorders-list'),
    re_path(r'^neworders/(?P<pk>\d+)/$', views.NewOrdersDetailView.as_view(), name='neworders-detail'),
    re_path(r'^closedorders/(?P<pk>\d+)/$', views.ClosedOrdersDetailView.as_view(), name='closedorders-detail'),
    re_path(r'^heldorders/(?P<pk>\d+)/$', views.HeldOrdersDetailView.as_view(), name='heldorders-detail'),
    re_path(r'^neworders/(?P<pk>\d+)/change/$', views.NewOrdersUpdatableDetailView.as_view(), name='neworders-detail-change'),
    re_path(r'^closedorders/(?P<pk>\d+)/change/$', views.ClosedOrdersUpdatableDetailView.as_view(), name='closedorders-detail-change'),
    re_path(r'^heldorders/(?P<pk>\d+)/change/$', views.HeldOrdersUpdatableDetailView.as_view(), name='heldorders-detail-change'),
    
    re_path(r'^neworders/(?P<orderitem_id>\d+)/close/$', views.CloseOrderAPI.as_view(), name='neworders-close'),
    re_path(r'^neworders/(?P<orderitem_id>\d+)/hold/$', views.HoldOrderAPI.as_view(), name='neworders-hold'),
    re_path(r'^closedorders/(?P<orderitem_id>\d+)/archive/$', views.ArchiveOrderAPI.as_view(), name='closedorders-archive'),
    re_path(r'^heldorders/(?P<orderitem_id>\d+)/unhold/$', views.UnholdOrderAPI.as_view(), name='heldorders-unhold'),

    re_path(r'^(?P<orderitem_id>\d+)/close/$', views.CloseOrderAPI.as_view(), name='order-close'),
    re_path(r'^(?P<orderitem_id>\d+)/hold/$', views.HoldOrderAPI.as_view(), name='order-hold'),
    re_path(r'^(?P<orderitem_id>\d+)/archive/$', views.ArchiveOrderAPI.as_view(), name='order-archive'),
    re_path(r'^(?P<orderitem_id>\d+)/unhold/$', views.UnholdOrderAPI.as_view(), name='order-unhold'),
]
