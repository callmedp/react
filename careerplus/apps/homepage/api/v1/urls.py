from django.conf.urls import url
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^static-site-page/(?P<pk>\d+)/$',
        views.StaticSiteView.as_view(), name='StaticSitePage'),
    
    url(r'^testimonial-category-map/$',
        views.TestimonialCategoryMapping.as_view(), name='testimonial-category-map'),

    ]