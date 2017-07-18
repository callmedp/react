from django.conf.urls import url
from .views import SearchListView, SearchQueryView

urlpatterns = [
    url(r'^results/$', SearchListView.as_view(), name='result_old'),
    url(r'^results/(?P<keyword_in_url>[-_./\w()]+)/$', SearchListView.as_view(), name='result'),
    url(r'^$', SearchQueryView.as_view()),
]
