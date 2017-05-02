from django.conf.urls import url
from .views import PageListPartial, PageDetailPartial, PageAddPartial

urlpatterns = [
	url(r'^page/$', PageListPartial.as_view(), name='page-list-partial'),
	url(r'^page/(?P<pk>\d+)/$', PageDetailPartial.as_view(), name='page-detail-partial'),
	url(r'^page/(?P<pk>\d+)/add/$', PageAddPartial.as_view(), name='page-add-partial'),
]
