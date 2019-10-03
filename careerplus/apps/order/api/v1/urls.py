from rest_framework import routers
from . import views
from django.conf.urls import url, include

router = routers.SimpleRouter()

router.register(r'orderitem', views.OrderItemViewSet)

urlpatterns = router.urls

urlpatterns = [
    url(r'^orderitem/$', views.OrderItemViewSet),
    url(r'^order/(?P<pk>\d+)/items/$', views.OrderItemsListView.as_view()),
    url(r'^(?P<pk>\d+)/update/$', views.OrderUpdateView.as_view()),
	url(r'^orderitemoperationsapi/$', views.OrderItemOperationApiView.as_view(),
		name='orderitemoperations'),
	url(r'^message-communications/$',
		views.MessageCommunicationListApiView.as_view(),
		name='message-communications'),

]