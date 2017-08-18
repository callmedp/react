from django.conf.urls import url
from .views import SearchListView

urlpatterns = [
    url(r'^recommended/(?P<f_area>[-./\w]+)/(?P<skill>[-./\w]+)$', SearchListView.as_view(), name='recommended_listing'),
    url(r'^results/$', SearchListView.as_view(), name='search_listing')
]
