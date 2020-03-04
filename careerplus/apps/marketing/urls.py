# python imports]

# django imports
# from django.conf.urls import url
from django.urls import re_path
from django.views.generic import RedirectView
from django.urls import reverse_lazy

# local imports
from . import views as marketing_views

# inter app imports

# third party imports

redirect_url_mapping = {"digital-marketing": "digital-marketing", "gst-cert": "gst-certification",
    "pmp-cert": "pmp-cert", "data-science-certification": "data-science-certification",
    "resume-writing": "resume-writing"}
app_name = 'marketing'
urlpatterns = [

                  #  marketing urls
                  re_path(r'^gst-certification$', marketing_views.MarketingPages.as_view(), name='gst-cert'),

                  re_path(r'^ifrs-cert$', marketing_views.MarketingPages.as_view(), name='ifrs-cert'),

                  re_path(r'^six-sigma-cert$', marketing_views.MarketingPages.as_view(), name='six-sigma-cert'),

                  re_path(r'^pmp-certification$', marketing_views.MarketingPages.as_view(), name='pmp-cert'),

                  re_path(r'^shrm-cert$', marketing_views.MarketingPages.as_view(), name='shrm-cert'),

                  re_path(r'^digital-marketing-cert$', marketing_views.MarketingPages.as_view(),
                      name='digital-marketing-certification'),

                  re_path(r'^data-science-certification$', marketing_views.MarketingPages.as_view(),
                      name='data-science-certification'),

                  re_path(r'^thankyou-for-query$', marketing_views.MarketingPages.as_view(), name='thankyou-for-query'),

                  re_path(r'^thank-you-1$', marketing_views.MarketingPages.as_view(), name='thank-you-1'),

                  re_path(r'^six-sigma-green-belt$', marketing_views.MarketingPages.as_view(), name='six-sigma-green-belt'),

                  re_path(r'^resume-writing-services$', marketing_views.MarketingPages.as_view(), name='resume-writing'),

                  re_path(r'^online-marketing$', marketing_views.MarketingPages.as_view(), name='digital-marketing'),

                  re_path(r'^aws-cert$', marketing_views.MarketingPages.as_view(), name='aws-cert'),

                  re_path(r'^aws-cert1$', marketing_views.MarketingPages.as_view(), name='aws-cert1'),
                  re_path(r'^ban-cert$', marketing_views.MarketingPages.as_view(), name='ban-cert'),
                  re_path(r'^data-science-cert$', marketing_views.MarketingPages.as_view(), name='data-science-cert'),
                  re_path(r'^data-science$', marketing_views.MarketingPages.as_view(), name='data-science'),

                  re_path(r'^international-resume-writing$', marketing_views.MarketingPages.as_view(),
                      name='international-resume-writing'),
                  re_path(r'^linkedin$', marketing_views.MarketingPages.as_view(), name='linkedin'),

                  re_path(r'^linkedin-1$', marketing_views.MarketingPages.as_view(), name='linkedin-1'),

                  re_path(r'^international-resume-writing-1', marketing_views.MarketingPages.as_view(),
                      name='international-resume-writing-1'),

                  re_path(r'^resume-writing-services-1$', marketing_views.MarketingPages.as_view(),
                      name='resume-writing-1'),

                  re_path(r'^devops-professional$', marketing_views.MarketingPages.as_view(), name='devops-professional'),

                  re_path(r'^data-scientist$', marketing_views.MarketingPages.as_view(), name='data-scientist'),

              ] + [re_path(r'^%s$' % key, marketing_views.MarketingPages.as_view()) for key, value in
                  redirect_url_mapping.items()]


