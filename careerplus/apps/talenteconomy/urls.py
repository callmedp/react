from django.conf.urls import url
from django.views.generic import TemplateView

# from .views import BlogLandingPageView, BlogLandingAjaxView,\
#     BlogDetailView, BlogDetailAjaxView,\
#     LoginToCommentView, ShowCommentBoxView, LoadMoreCommentView,\
#     BlogTagListView, RegisterToCommentView



urlpatterns = [
     url(r'^$', TemplateView.as_view(template_name="main.html"), name='talent-landing'),

    

]


# mobile page url

urlpatterns += [
    
]
