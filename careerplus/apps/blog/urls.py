from django.conf.urls import url

from .views import BlogLandingPageView, BlogLandingAjaxView
from .adminview import BlogAddView

urlpatterns = [
    url(r'^$', BlogLandingPageView.as_view(), name='blog-landing'),
    url(r'^category-wise-loading/$', BlogLandingAjaxView.as_view(),
    	name='blog-landing-load'),

    url(r'^admin/$', BlogAddView.as_view(),
    	name='blog-add'),
]
