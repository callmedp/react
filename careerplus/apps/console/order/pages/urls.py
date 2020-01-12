from django.conf.urls import url
from .import views
app_name='console'
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
    
    url(r'^neworders/(?P<orderitem_id>\d+)/close/$', views.CloseOrderAPI.as_view(), name='neworders-close'),
    url(r'^neworders/(?P<orderitem_id>\d+)/hold/$', views.HoldOrderAPI.as_view(), name='neworders-hold'),
    url(r'^closedorders/(?P<orderitem_id>\d+)/archive/$', views.ArchiveOrderAPI.as_view(), name='closedorders-archive'),
    url(r'^heldorders/(?P<orderitem_id>\d+)/unhold/$', views.UnholdOrderAPI.as_view(), name='heldorders-unhold'),

    url(r'^(?P<orderitem_id>\d+)/close/$', views.CloseOrderAPI.as_view(), name='order-close'),
    url(r'^(?P<orderitem_id>\d+)/hold/$', views.HoldOrderAPI.as_view(), name='order-hold'),
    url(r'^(?P<orderitem_id>\d+)/archive/$', views.ArchiveOrderAPI.as_view(), name='order-archive'),
    url(r'^(?P<orderitem_id>\d+)/unhold/$', views.UnholdOrderAPI.as_view(), name='order-unhold'),
]
