from django.conf.urls import url
from django.views.generic import TemplateView

from .views import HRLandingView, HRBlogDetailView

urlpatterns = [
     url(r'^$', HRLandingView.as_view(), name='hr-landing'),
     url(r'^(?P<cat_slug>[-\w]+)/(?P<slug>[-\w]+)/$', 
     	HRBlogDetailView.as_view(), name='hr-articles-detail'),

]


# mobile page url

urlpatterns += [
    
]