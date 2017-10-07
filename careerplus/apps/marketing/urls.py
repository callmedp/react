from django.conf.urls import url

from . import views as marketing_views


urlpatterns = [

    #  marketing urls
    url(r'^gst-cert$',
        marketing_views.MarketingPages.as_view(),
        name='gst-cert'),

    url(r'^ifrs-cert$',
        marketing_views.MarketingPages.as_view(),
        name='ifrs-cert'),

    url(r'^six-sigma-cert$',
        marketing_views.MarketingPages.as_view(),
        name='six-sigma-cert'),

    url(r'^pmp-cert$',
        marketing_views.MarketingPages.as_view(),
        name='pmp-cert'),

    url(r'^shrm-cert$',
        marketing_views.MarketingPages.as_view(),
        name='shrm-cert'),

    url(r'^digital-marketing-certification$',
        marketing_views.MarketingPages.as_view(),
        name='digital-marketing-certification'),

    url(r'^thankyou-for-query$',
        marketing_views.MarketingPages.as_view(),
        name='thankyou-for-query'),
]