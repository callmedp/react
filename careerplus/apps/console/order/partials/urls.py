# from django.conf.urls import url
from django.urls import re_path
from . import views
app_name = 'console'
urlpatterns = [
	re_path(r'^neworders/$', views.NewOrdersListPartial.as_view(), name='neworders-list-partial'),
	re_path(r'^closedorders/$', views.ClosedOrdersListPartial.as_view(), name='closedorders-list-partial'),
	re_path(r'^heldorders/$', views.HeldOrdersListPartial.as_view(), name='heldorders-list-partial'),
	re_path(r'^neworders/(?P<pk>\d+)/$', views.NewOrdersDetailPartial.as_view(), name='neworders-detail-partial'),
	re_path(r'^closedorders/(?P<pk>\d+)/$', views.ClosedOrdersDetailPartial.as_view(), name='closedorders-detail-partial'),
	re_path(r'^heldorders/(?P<pk>\d+)/$', views.HeldOrdersDetailPartial.as_view(), name='heldorders-detail-partial'),
	re_path(r'^neworders/(?P<pk>\d+)/change/$', views.NewOrdersUpdatableDetailPartial.as_view(), name='neworders-detail-change-partial'),
	re_path(r'^closedorders/(?P<pk>\d+)/change/$', views.ClosedOrdersUpdatableDetailPartial.as_view(), name='closedorders-detail-change-partial'),
	re_path(r'^heldorders/(?P<pk>\d+)/change/$', views.HeldOrdersUpdatableDetailPartial.as_view(), name='heldorders-detail-change-partial'),
	
]
