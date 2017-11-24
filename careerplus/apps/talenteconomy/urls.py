from django.conf.urls import url
from django.views.generic import TemplateView

from .views import TalentEconomyLandingView, TEBlogCategoryListView,\
     TEBlogDetailView
#     LoginToCommentView, ShowCommentBoxView, LoadMoreCommentView,\
#     BlogTagListView, RegisterToCommentView



urlpatterns = [
     url(r'^$', TalentEconomyLandingView.as_view(), name='talent-landing'),
     url(r'^(?P<cat_slug>[-\w]+)/(?P<slug>[-\w]+)/$',
        TEBlogDetailView.as_view(), name='te-articles-detail'),
     url(r'^(?P<slug>[-\w]+)/$', TEBlogCategoryListView.as_view(),
        name='te-articles-by-category'),

]


# mobile page url

urlpatterns += [
    
]
