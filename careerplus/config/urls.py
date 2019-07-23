"""careerplus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.decorators.cache import cache_page
from django.contrib.sitemaps import views as sitemaps_views

from ckeditor_uploader import views as ckeditor_views

from users.views import (
    RegistrationApiView, LoginApiView, LogoutApiView)

from console.welcomecall.views import ShowNumberField

from homepage import views as homepage_view
from linkedin.views import AutoLoginView
from shop.views import ProductDetailView, CourseCatalogueView
from users.views import LinkedinCallbackView, UserLoginTokenView
from search.views import FuncAreaPageView
from blog import views as blog_view
from skillpage.views import (
    ServiceDetailPage, UniversityPageView,
    UniversityFacultyView, LocationSkillPageView)

from resumebuilder.views import (WriteResumeView)

from django.conf.urls import (
    handler400, handler403, handler404, handler500
)
from seo.sitemap import (
    CourseSitemap, SkillSitemap,
    CategorySitemap, ServiceSitemap,
    ArticleSitemap, ArticleCategorySitemap,
    CMSSitemap, TalentEconomySitemap, TalentCategorySitemap,
    TalentAuthorSitemap)

handler404 = 'users.views.page_not_found'
handler500 = 'users.views.server_error'

course_sitemap = {
   'course': CourseSitemap,
   'skill': SkillSitemap,
   'category': CategorySitemap
}

service_sitemap = {
   'service': ServiceSitemap,
}

article_sitemap = {
   'article': ArticleSitemap,
   'category': ArticleCategorySitemap,
}

cms_sitemap = {
   'service': CMSSitemap,
}

talent_sitemap = {
   'talenteconomy': TalentEconomySitemap,
   'category': TalentCategorySitemap,
   'author': TalentAuthorSitemap
}



#Library Patches
from .startup_script import apply_patch
apply_patch()

urlpatterns = [url(r'^services/%s/%s/$' %(cat_slug,cat_id),
        ServiceDetailPage.as_view())  for cat_id,cat_slug in settings.SERVICE_PAGE_ID_SLUG_MAPPING.items()]

# Product Detail URLs
urlpatterns += [
    url(r'^robots.txt$', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain')),
    url(r'^certification_course_sitemap\.xml$', cache_page(settings.SITEMAP_CACHING_TIME)(sitemaps_views.sitemap), {
        'sitemaps': course_sitemap,
        'template_name': 'sitemap.xml'}, name='sitemap'),
    url(r'^job_services_sitemap\.xml$', cache_page(settings.SITEMAP_CACHING_TIME)(sitemaps_views.sitemap), {
        'sitemaps': service_sitemap,
        'template_name': 'sitemap.xml'}, name='sitemap'),
    url(r'^article_sitemap\.xml$', cache_page(settings.SITEMAP_CACHING_TIME)(sitemaps_views.sitemap), {
        'sitemaps': article_sitemap,
        'template_name': 'sitemap.xml'}, name='sitemap'),
    url(r'^cms_sitemap\.xml$', cache_page(settings.SITEMAP_CACHING_TIME)(sitemaps_views.sitemap), {
        'sitemaps': cms_sitemap,
        'template_name': 'sitemap.xml'}, name='sitemap'),
    url(r'^te_sitemap\.xml$', cache_page(settings.SITEMAP_CACHING_TIME)(sitemaps_views.sitemap), {
        'sitemaps': talent_sitemap,
        'template_name': 'sitemap.xml'}, name='sitemap'),

    url(r'^course/(?P<cat_slug>[\w-]+)/(?P<prd_slug>[\w-]+)/pd-(?P<pk>[\d]+)$',
        ProductDetailView.as_view(), name='course-detail'),

    url(r'^services/(?P<cat_slug>[\w-]+)/(?P<prd_slug>[\w-]+)/pd-(?P<pk>[\d]+)$',
        ProductDetailView.as_view(), name='service-detail'),
    url(r'^courses/', include('skillpage.urls', namespace='skillpage')),
    url(r'^university/faculty/(?P<faculty_slug>[-\w]+)/(?P<pk>\d+)/$',
        UniversityFacultyView.as_view(), name='university-faculty'),
    url(r'^university/(?P<fa_slug>[-\w]+)/(?P<university_slug>[-\w]+)/(?P<pk>\d+)/$',
        UniversityPageView.as_view(), name='university-page'),
    url(r'^services/(?P<fa_slug>[-\w]+)/(?P<pk>\d+)/$',
        FuncAreaPageView.as_view(), name='func_area_results'),

    url(r'^online-courses.html$',
        CourseCatalogueView.as_view(), name='course-catalogoue'),

    url(r'^courses/(?P<sc_slug>[a-z\-]+)/$', LocationSkillPageView.as_view(), name='location-skillpage'),



    # url(r'^job-assistance/(?P<cat_slug>[\w-]+)/(?P<prd_slug>[\w-]+)/pd-(?P<pk>[\d]+)$',
    #     ProductDetailView.as_view(), name='job-assist-detail'),
    # url(r'^product/(?P<cat_slug>[\w-]+)/(?P<prd_slug>[\w-]+)/pd-(?P<pk>[\d]+)$',
    #     ProductDetailView.as_view(), name='other-detail'),

]

# Additional admin urls
_admin_site_get_urls = admin.site.get_urls


def get_urls():
    from django.conf.urls import url
    urls = _admin_site_get_urls()
    urls += [
        url(r'^autologintoken/$',
            admin.site.admin_view(UserLoginTokenView.as_view())),
        url(r'^shownumberfield/$',admin.site.admin_view(ShowNumberField.as_view()))
    ]
    return urls

admin.site.get_urls = get_urls

urlpatterns += [
                   url(r'^admin/', include(admin.site.urls)),
                   url(r'^api-auth/',
                       include('rest_framework.urls', namespace='rest_framework')),
                   url(r'api/v1/', include('shop.api.v1.urls', namespace='shop-api')),
                   url(r'^$', homepage_view.HomePageView.as_view(), name='homepage'),
                   url(r'^console/', include('console.urls', namespace='console')),
                   url(r'^shop/', include('shop.urls', namespace='shop')),
                   url(r'^user/', include('users.urls', namespace='users')),
                   url(r'^cms/', include('cms.urls', namespace='cms')),
                   url(r'^article/', include('blog.urls', namespace='blog')),
                   url(r'^talenteconomy/', include('talenteconomy.urls', namespace='talent')),
                   url(r'^hr-insider/', include('hrinsider.urls', namespace='hrinsider')),

                   url(r'^cart/', include('cart.urls', namespace='cart')),
                   url(r'^order/', include('order.urls', namespace='order')),
                   url(r'^geolocation/', include('geolocation.urls', namespace='geolocation')),
                   url(r'^payment/', include('payment.urls', namespace='payment')),
                   url(r'^ajax/', include('ajax.urls', namespace='ajax')),
                   url(r'^design/', include('design.urls', namespace='design')),
                   url(r'^ckeditor/upload/', login_required(ckeditor_views.upload), name='ckeditor_upload'),
                   url(r'^ckeditor/bbrowse/', login_required(ckeditor_views.browse), name='ckeditor_browse'),
                   url(r'^search/', include('search.urls', namespace='search')),
                   url(r'^partner/', include('partner.urls')),
                   url(r'^partner/', include('microsite.urls')),
                   url(r'^linkedin/', include('linkedin.urls')),
                   url(r'^register/$', RegistrationApiView.as_view(), name='register'),
                   url(r'^login/$', LoginApiView.as_view(), name='login'),
                   url(r'^logout/$', LogoutApiView.as_view(), name='logout'),
                   url(r'^dashboard/', include('dashboard.urls', namespace='dashboard')),
                   url(r'^autologin/(?P<token>.+)/$', AutoLoginView.as_view(), name='autologin'),
                   url(r'^linkedin/login/$',
                       LinkedinCallbackView.as_view(), name='linkedin-login'),
                  url(r'^api/v1/resume/', include('resumebuilder.api.v1.urls', namespace='resume_builder')),

                   url(r'^api/', include('api.urls', namespace='api')),

                   url(r'^lead/', include('crmapi.urls', namespace='crmapi')),

                   url(r'^', include('marketing.urls', namespace='marketing')),

                   url(r'^about-us$',
                       homepage_view.AboutUsView.as_view(), name='about-us'),
                   url(r'^disclaimer$',
                       homepage_view.DisclaimerView.as_view(), name='disclaimer'),

                   url(r'^privacy-policy$',
                       homepage_view.PrivacyPolicyView.as_view(),
                       name='privacy-policy'),
                   url(r'^tnc$',
                       homepage_view.TermsConditionsView.as_view(),
                       name='tnc'),
                   url(r'^contact-us$',
                       homepage_view.ContactUsView.as_view(),
                       name='contact-us'),

                   url(r'^article-categories/(?P<slug>[-\w]+)/$',
                       blog_view.BlogCategoryListView.as_view(),
                       name='articles-by-category'),

                   # django-oauth-toolkit
                   url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

                   # entry point for react template
                   url(r'^resume-builder/', WriteResumeView.as_view())

] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
) + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
) + static(settings.DOWNLOAD_URL, document_root=settings.DOWNLOAD_ROOT)

if settings.DEBUG:
    import debug_toolbar

    from rest_framework.response import Response
    from rest_framework.schemas import SchemaGenerator
    from rest_framework.views import APIView
    from rest_framework_swagger import renderers
    from rest_framework_swagger.views import get_swagger_view

    schema_view = get_swagger_view(title='Shine Learning API Docs')


    class SwaggerSchemaView(APIView):
        renderer_classes = [
        #     renderers.OpenAPIRenderer,
            renderers.SwaggerUIRenderer
        ]

        authentication_classes = []
        permission_classes = []

        def get(self, request):
            generator = SchemaGenerator(title="Learning API Docs")
            schema = generator.get_schema(request=request)

            return Response(schema)


    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                      url(r'^api-docs/', schema_view),
                  ] + urlpatterns


import logging
from sorl.thumbnail.log import ThumbnailLogHandler

handler = ThumbnailLogHandler()
handler.setLevel(logging.ERROR)
logging.getLogger('sorl.thumbnail').addHandler(handler)
