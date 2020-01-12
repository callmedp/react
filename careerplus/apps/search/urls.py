from django.conf.urls import url
from .views import SearchListView, RecommendedSearchView, RedirectToRecommendationsView
app_name='search'
urlpatterns = [
    # url(r'^recommended/(?P<area_slug>[-./\w+\(\)]+)-(?P<area>[\d]+)/(?P<skills_slug>[-./\w+]+)_(?P<skills>[-\d]+)/$',
    #     RecommendedSearchView.as_view(), name='recommended_listing'),
    url(r'^results/$', SearchListView.as_view(), name='search_listing'),
    # url(r'^redirect-to-recommendations/$', RedirectToRecommendationsView.as_view(), name='recommend')
]
