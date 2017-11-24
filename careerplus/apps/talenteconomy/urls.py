from django.conf.urls import url
from django.views.generic import TemplateView

from .views import TalentEconomyLandingView, TEBlogCategoryListView
#     BlogDetailView, BlogDetailAjaxView,\
#     LoginToCommentView, ShowCommentBoxView, LoadMoreCommentView,\
#     BlogTagListView, RegisterToCommentView



urlpatterns = [
     url(r'^$', TalentEconomyLandingView.as_view(), name='talent-landing'),
     url(r'^(?P<slug>[-\w]+)/$', TEBlogCategoryListView.as_view(),
        name='te-articles-by-category'),

]


# mobile page url

urlpatterns += [
    
]
