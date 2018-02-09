from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^v1/create-order/$',
        views.CreateOrderApiView.as_view(), name='api-createorder'),
    url(r'^v1/get-ltvalue/$',
        views.EmailLTValueApiView.as_view(), name='api-ltvalue'),
    url(r'^v1/history/$',
        views.OrderHistoryAPIView.as_view(), name='historylist'),
]