from django.conf.urls import url
from .views import SearchListView, SearchQueryView

urlpatterns = [
    url(r'^recommended/(?P<f_area>[-./\w]+)/(?P<skill>[-./\w]+)$', SearchListView.as_view(), name='recommended_listing'),
    url(r'^results/(?P<keyword_in_url>[-_./\w()]+)/$', SearchListView.as_view(), name='search_listing')
]
