from django.conf.urls import url
from django.views.generic import TemplateView

from .views import TalentEconomyLandingView
#     BlogDetailView, BlogDetailAjaxView,\
#     LoginToCommentView, ShowCommentBoxView, LoadMoreCommentView,\
#     BlogTagListView, RegisterToCommentView



urlpatterns = [
     url(r'^$', TalentEconomyLandingView.as_view(), name='talent-landing'),
     url(r'^category/', TemplateView.as_view(template_name="talenteconomy/category.html"), name='category-landing'),

]


# mobile page url

urlpatterns += [
    
]
