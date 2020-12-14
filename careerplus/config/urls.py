"""careerplus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  re_path(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  re_path(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  re_path(r'^blog/', include('blog.urls'))
"""
# from django.conf.urls import url, include
from django.urls import re_path, include
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
from shop.views import ProductDetailView, CourseCatalogueView, GoogleResumeAdView, SmsUrlRedirect
from users.views import LinkedinCallbackView, UserLoginTokenView,CourseServiceWhatsappBtn
from search.views import FuncAreaPageView
from skillpage.views import SkillPageReactView
from blog import views as blog_view
from skillpage.views import (
    ServiceDetailPage, UniversityPageView,
    UniversityFacultyView, LocationSkillPageView)

from resumebuilder.views import (WriteResumeView,FreeResumeDownload)

from resumescorechecker.views import (ScoreCheckerView, ScoreCheckerView2, ScoreCheckerViewMobile)

from django.conf.urls import (
    handler400, handler403, handler404, handler500
)
# from django.urls import (
#     handler400, handler403, handler404, handler500
# )

from seo.sitemap import (
    CourseSitemap, SkillSitemap,
    CategorySitemap, ServiceSitemap,
    ArticleSitemap, ArticleCategorySitemap,
    CMSSitemap, TalentEconomySitemap, TalentCategorySitemap,
    TalentAuthorSitemap,PracticeTestCategorySitemap,PracticeTestExamSitemap,
    PracticeTestSubCategorySitemap, ResumeBuilderSitemap)

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
practicetest_sitemap = {
    'category':     PracticeTestCategorySitemap,
    'sub-category': PracticeTestSubCategorySitemap,
    'practice-test-exam': PracticeTestExamSitemap
}

builder_sitemap = {
    'resume-builder' : ResumeBuilderSitemap
}

# Library Patches
from .startup_script import apply_patch

apply_patch()

urlpatterns = [re_path(r'^services/%s/%s/$' % (cat_slug, cat_id),
                   ServiceDetailPage.as_view()) for cat_id, cat_slug in settings.SERVICE_PAGE_ID_SLUG_MAPPING.items()]

# Product Detail URLs
urlpatterns += [
    re_path(r'^robots.txt$', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain')),
    re_path(r'^certification_course_sitemap\.xml$',
        cache_page(settings.SITEMAP_CACHING_TIME)(sitemaps_views.sitemap), {
            'sitemaps': course_sitemap,
            'template_name': 'sitemap.xml'}, name='sitemap'),
    re_path(r'^job_services_sitemap\.xml$', 
        cache_page(settings.SITEMAP_CACHING_TIME)(sitemaps_views.sitemap), {
            'sitemaps': service_sitemap,
            'template_name': 'sitemap.xml'}, name='sitemap'),
    re_path(r'^article_sitemap\.xml$', 
        cache_page(settings.SITEMAP_CACHING_TIME)(sitemaps_views.sitemap), {
            'sitemaps': article_sitemap,
            'template_name': 'sitemap.xml'}, name='sitemap'),
    re_path(r'^cms_sitemap\.xml$', 
        cache_page(settings.SITEMAP_CACHING_TIME)(sitemaps_views.sitemap), {
            'sitemaps': cms_sitemap,
            'template_name': 'sitemap.xml'}, name='sitemap'),
    re_path(r'^te_sitemap\.xml$', 
        cache_page(settings.SITEMAP_CACHING_TIME)(sitemaps_views.sitemap), {
            'sitemaps': talent_sitemap,
            'template_name': 'sitemap.xml'}, name='sitemap'),
    re_path(r'^practice-tests\.xml$', 
        cache_page(settings.SITEMAP_CACHING_TIME)(sitemaps_views.sitemap), {
            'sitemaps': practicetest_sitemap,
            'template_name': 'sitemap.xml'}, name='sitemap'),
    re_path(r'^builder\.xml$',
        cache_page(settings.SITEMAP_CACHING_TIME)(sitemaps_views.sitemap), {
            'sitemaps': builder_sitemap,
            'template_name': 'sitemap.xml'}, name='sitemap'),

    re_path(r'^course/(?P<cat_slug>[\w-]+)/(?P<prd_slug>[\w-]+)/pd-(?P<pk>[\d]+)$',
        ProductDetailView.as_view(), name='course-detail'),

    re_path(r'^services/(?P<cat_slug>[\w-]+)/(?P<prd_slug>[\w-]+)/pd-(?P<pk>[\d]+)$',
        ProductDetailView.as_view(), name='service-detail'),

    re_path(r'^services/(?P<fa_slug>[-\w]+)/(?P<pk>\d+)/$',
        FuncAreaPageView.as_view(), name='func_area_results'),
    re_path(r'^services/(?P<cat_slug>[\w-]+)/(?P<country>[\w-]+)/$',
        GoogleResumeAdView.as_view(), name='google-resume-ad'),
    re_path(r'^courses/(?P<fa_slug>[-\w]+)/(?P<skill_slug>[-\w]+)/(?P<pk>\d+)/$', SkillPageReactView.as_view()),
    re_path(r'^courses/', include('skillpage.urls',
                              namespace='skillpage')),
    re_path(r'^university/faculty/(?P<faculty_slug>[-\w]+)/(?P<pk>\d+)/$',
        UniversityFacultyView.as_view(), name='university-faculty'),
    re_path(r'^university/(?P<fa_slug>[-\w]+)/(?P<university_slug>[-\w]+)/(?P<pk>\d+)/$',
        UniversityPageView.as_view(), name='university-page'),

    re_path(r'^online-courses.html$',
        CourseCatalogueView.as_view(), name='course-catalogoue'),
    
    re_path(r'^services/(?P<cat_slug>[\w-]+)/(?P<country>[\w-]+)/$',
            GoogleResumeAdView.as_view(), name='google-resume-ad'),

    re_path(r'^courses/(?P<sc_slug>[a-z\-]+)/$', 
        LocationSkillPageView.as_view(), 
        name='location-skillpage'),

    re_path(r'^', include('assessment.urls',
                      namespace='assessment')),

    # re_path(r'^job-assistance/(?P<cat_slug>[\w-]+)/(?P<prd_slug>[\w-]+)/pd-(?P<pk>[\d]+)$',
    #     ProductDetailView.as_view(), name='job-assist-detail'),
    # re_path(r'^product/(?P<cat_slug>[\w-]+)/(?P<prd_slug>[\w-]+)/pd-(?P<pk>[\d]+)$',
    #     ProductDetailView.as_view(), name='other-detail'),

]

# Additional admin urls
_admin_site_get_urls = admin.site.get_urls


def get_urls():
    # from django.conf.urls import url
    urls = _admin_site_get_urls()
    urls += [
        re_path(r'^autologintoken/$',
            admin.site.admin_view(UserLoginTokenView.as_view())),
        re_path(r'^shownumberfield/$', admin.site.admin_view(ShowNumberField.as_view())),
        re_path(r'^whatsappbtn/$', admin.site.admin_view(CourseServiceWhatsappBtn.as_view())),
        re_path(r'^free-resume-downloads/$', admin.site.admin_view(FreeResumeDownload.as_view())),
    ]
    return urls


admin.site.get_urls = get_urls

urlpatterns += [
                   re_path(r'^admin/', admin.site.urls),
                   re_path(r'^api-auth/',include('rest_framework.urls', namespace='rest_framework')),
                   re_path(r'api/v1/', include('shop.api.v1.urls', namespace='shop-api')),
                   re_path(r'api/v2/', include('shop.api.v2.urls', namespace='shop-api')),
                   re_path(r'api/', include('skillpage.api.v1.urls', namespace='skillpage-api')),
                   re_path(r'^$', homepage_view.HomePageView.as_view(), name='homepage'),
                   re_path(r'^console/', include('console.urls', namespace='console')),
                   re_path(r'^shine/', include('shine.urls', namespace='shine')),
                   re_path(r'^shop/', include('shop.urls', namespace='shop')),
                   re_path(r'^', include('shop.urls', namespace='shop')),
                   re_path(r'^user/', include('users.urls', namespace='users')),
                   re_path(r'^cms/', include('cms.urls', namespace='cms')),
                   re_path(r'^article/', include('blog.urls', namespace='blog')),
                   re_path(r'^talenteconomy/', include('talenteconomy.urls', namespace='talent')),
                   re_path(r'^hr-insider/', include('hrinsider.urls', namespace='hrinsider')),
                   re_path(r'^cart/', include('cart.urls', namespace='cart')),
                   re_path(r'^order/', include('order.urls', namespace='order')),

                   re_path(r'^api/', include('order.api.urls', namespace='api')),
                   re_path(r'^geolocation/', include('geolocation.urls', namespace='geolocation')),
                   re_path(r'^payment/', include('payment.urls', namespace='payment')),
                   re_path(r'^ajax/', include('ajax.urls', namespace='ajax')),
                   re_path(r'^design/', include('design.urls', namespace='design')),
                   re_path(r'^ckeditor/upload/', login_required(ckeditor_views.upload), name='ckeditor_upload'),
                   re_path(r'^ckeditor/bbrowse/', login_required(ckeditor_views.browse), name='ckeditor_browse'),
                   re_path(r'^search/', include('search.urls', namespace='search')),
                   re_path(r'^partner/', include('partner.urls')),
                   re_path(r'^partner/', include('microsite.urls')),
                   re_path(r'^linkedin/', include('linkedin.urls')),
                   re_path(r'^register/$', RegistrationApiView.as_view(), name='register'),
                   re_path(r'^login/$', LoginApiView.as_view(), name='login'),
                   re_path(r'^logout/$', LogoutApiView.as_view(), name='logout'),
                   re_path(r'^dashboard/', include('dashboard.urls', namespace='dashboard')),
                   re_path(r'^autologin/(?P<token>.+)/$', AutoLoginView.as_view(), name='autologin'),
                   re_path(r'^linkedin/login/$',
                       LinkedinCallbackView.as_view(), name='linkedin-login'),
                   re_path(r'^api/v1/resume/', include('resumebuilder.api.v1.urls', namespace='resume_builder')),

                   re_path(r'^api/v1/geolocation/', include('geolocation.api.v1.urls', namespace='geolocation')),

                   re_path(r'^api/v1/cart/', include('cart.api.v1.urls', namespace='cart')),

                   re_path(r'^api/v1/coupon/', include('coupon.api.v1.urls', namespace='coupon')),

                   re_path(r'^api/v1/wallet/', include('wallet.api.v1.urls', namespace='wallet')),

                   re_path(r'^api/', include('api.urls', namespace='api')),
                   re_path(r'^api/', include('homepage.api.urls', namespace='api')),

                   re_path(r'^lead/', include('crmapi.urls', namespace='crmapi')),

                    re_path(r'^api/', include('wallet.urls')),

                    re_path(r'^', include('marketing.urls', namespace='marketing')),


                   re_path(r'^about-us$',
                       homepage_view.AboutUsView.as_view(), name='about-us'),

                   re_path(r'^contact-us$',
                       homepage_view.ContactUsView.as_view(),
                       name='contact-us'),

                   re_path(r'^article-categories/(?P<slug>[-\w]+)/$',
                       blog_view.BlogCategoryListView.as_view(),
                       name='articles-by-category'),

                   # django-oauth-toolkit
                   re_path(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

                   # entry point for react template
                   re_path(r'^resume-builder/', WriteResumeView.as_view()),

                   #resume score checker 
                   re_path(r'^resume-score-checker/', ScoreCheckerView.as_view()),
                   re_path(r'^api/', include(('resumescorechecker.api.urls','resumescorechecker'), 
                                namespace='resume_score_checker')),
                   re_path(r'^(?P<url_id>\d+)/(?P<encoded_mobile>[-\w]+)/$', SmsUrlRedirect.as_view())

                #    #resume score checker 
                #    re_path(r'^result-page/', ScoreCheckerView2.as_view()),

                #    #resume score checker Mobile
                #    re_path(r'^score-checker/', ScoreCheckerViewMobile.as_view()),

                   
                   

               ]
if settings.DEBUG:
    urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT,
) + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
) + static(settings.DOWNLOAD_URL, document_root=settings.DOWNLOAD_ROOT)
  
urlpatterns += [re_path(r'^(?P<page_slug>tnc|disclaimer|privacy-policy)/$',
         homepage_view.StaticSiteContentView.as_view(),
         name='static-site-content')]

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
                      re_path(r'^__debug__/', include(debug_toolbar.urls)),
                      re_path(r'^api-docs/', schema_view),
                  ] + urlpatterns

import logging
from sorl.thumbnail.log import ThumbnailLogHandler

handler = ThumbnailLogHandler()
handler.setLevel(logging.ERROR)
logging.getLogger('sorl.thumbnail').addHandler(handler)
