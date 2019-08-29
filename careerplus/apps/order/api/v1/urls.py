from rest_framework import routers
from . import views
from django.conf.urls import url

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^orderitem/$', views.OrderItemViewSet),
    url(r'^order/(?P<pk>\d+)/items/$', views.OrderItemsListView.as_view()),
    url(r'^order/(?P<pk>\d+)/update/$', views.OrderUpdateView.as_view()),
]