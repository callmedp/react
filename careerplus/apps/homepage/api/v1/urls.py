# from django.conf.urls import url
from django.urls import re_path
from django.conf import settings

from . import views
app_name = "homepage"
urlpatterns = [
    re_path(r'^static-site-page/(?P<page_type>\d+)/$',
        views.StaticSiteView.as_view(), name='StaticSitePage'),
    
    re_path(r'^testimonial-category-map/$',
        views.TestimonialCategoryMapping.as_view(), name='testimonial-category-map'),

    ]