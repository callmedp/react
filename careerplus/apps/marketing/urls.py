# python imports]

# django imports
from django.conf.urls import url
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
                  url(r'^gst-certification$', marketing_views.MarketingPages.as_view(), name='gst-cert'),

                  url(r'^ifrs-cert$', marketing_views.MarketingPages.as_view(), name='ifrs-cert'),

                  url(r'^six-sigma-cert$', marketing_views.MarketingPages.as_view(), name='six-sigma-cert'),

                  url(r'^pmp-certification$', marketing_views.MarketingPages.as_view(), name='pmp-cert'),

                  url(r'^shrm-cert$', marketing_views.MarketingPages.as_view(), name='shrm-cert'),

                  url(r'^digital-marketing-cert$', marketing_views.MarketingPages.as_view(),
                      name='digital-marketing-certification'),

                  url(r'^data-science-certification$', marketing_views.MarketingPages.as_view(),
                      name='data-science-certification'),

                  url(r'^thankyou-for-query$', marketing_views.MarketingPages.as_view(), name='thankyou-for-query'),

                  url(r'^thank-you-1$', marketing_views.MarketingPages.as_view(), name='thank-you-1'),

                  url(r'^six-sigma-green-belt$', marketing_views.MarketingPages.as_view(), name='six-sigma-green-belt'),

                  url(r'^resume-writing-services$', marketing_views.MarketingPages.as_view(), name='resume-writing'),

                  url(r'^online-marketing$', marketing_views.MarketingPages.as_view(), name='digital-marketing'),

                  url(r'^aws-cert$', marketing_views.MarketingPages.as_view(), name='aws-cert'),

                  url(r'^aws-cert1$', marketing_views.MarketingPages.as_view(), name='aws-cert1'),
                  url(r'^ban-cert$', marketing_views.MarketingPages.as_view(), name='ban-cert'),
                  url(r'^data-science-cert$', marketing_views.MarketingPages.as_view(), name='data-science-cert'),
                  url(r'^data-science$', marketing_views.MarketingPages.as_view(), name='data-science'),

                  url(r'^international-resume-writing$', marketing_views.MarketingPages.as_view(),
                      name='international-resume-writing'),
                  url(r'^linkedin$', marketing_views.MarketingPages.as_view(), name='linkedin'),

                  url(r'^linkedin-1$', marketing_views.MarketingPages.as_view(), name='linkedin-1'),

                  url(r'^international-resume-writing-1', marketing_views.MarketingPages.as_view(),
                      name='international-resume-writing-1'),

                  url(r'^resume-writing-services-1$', marketing_views.MarketingPages.as_view(),
                      name='resume-writing-1'),

                  url(r'^devops-professional$', marketing_views.MarketingPages.as_view(), name='devops-professional'),

                  url(r'^data-scientist$', marketing_views.MarketingPages.as_view(), name='data-scientist'),

              ] + [url(r'^%s$' % key, marketing_views.MarketingPages.as_view()) for key, value in
                  redirect_url_mapping.items()]


