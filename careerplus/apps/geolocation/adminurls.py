from django.conf.urls import url
from .adminviews import CountryListView, CountryUpdateView


urlpatterns = [
	url(r'^country-list/$', CountryListView.as_view(), name='counry-list'),

    url(r'^country/(?P<pk>\d+)/change/$', CountryUpdateView.as_view(),
        name='country-update'),
]