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

from ckeditor_uploader import views as ckeditor_views

from users.views import (
    RegistrationApiView, LoginApiView, LogoutApiView)
from homepage.views import HomePageView
from linkedin.views import AutoLoginView
from shop.views import ProductDetailView
from users.views import LinkedinCallbackView
from search.views import FuncAreaPageView
from django.conf.urls import (
    handler400, handler403, handler404, handler500
)

handler404 = 'users.views.page_not_found'
handler500 = 'users.views.server_error'

urlpatterns = []

# Product Detail URLs
urlpatterns += [
    url(r'^course/(?P<cat_slug>[\w-]+)/(?P<prd_slug>[\w-]+)/pd-(?P<pk>[\d]+)$',
        ProductDetailView.as_view(), name='course-detail'),
    url(r'^resume/(?P<cat_slug>[\w-]+)/(?P<prd_slug>[\w-]+)/pd-(?P<pk>[\d]+)$',
        ProductDetailView.as_view(), name='resume-detail'),
    url(r'^job-assistance/(?P<cat_slug>[\w-]+)/(?P<prd_slug>[\w-]+)/pd-(?P<pk>[\d]+)$',
        ProductDetailView.as_view(), name='job-assist-detail'),
    url(r'^product/(?P<cat_slug>[\w-]+)/(?P<prd_slug>[\w-]+)/pd-(?P<pk>[\d]+)$',
        ProductDetailView.as_view(), name='other-detail'),
]

urlpatterns += [
    url(r'^(?P<fa_slug>[-\w]+)-courses/(?P<pk>\d+)/$', FuncAreaPageView.as_view(), name='func_area_results'),
]
urlpatterns += [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', HomePageView.as_view(), name='homepage'),
    url(r'^console/', include('console.urls', namespace='console')),
    url(r'^shop/', include('shop.urls', namespace='shop')),
    url(r'^user/', include('users.urls', namespace='users')),
    url(r'^cms/', include('cms.urls', namespace='cms')),
    url(r'^skillpage/', include('skillpage.urls', namespace='skillpage')),
    url(r'^article/', include('blog.urls', namespace='blog')),
    url(r'^shop/', include('shop.urls', namespace='shop')),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^order/', include('order.urls', namespace='order')),
    url(r'^geolocation/', include('geolocation.urls', namespace='geolocation')),
    url(r'^payment/', include('payment.urls', namespace='payment')),
    url(r'^ajax/', include('ajax.urls', namespace='ajax')),
    url(r'^design/', include('design.urls', namespace='design')),

    url(r'^ckeditor/upload/', login_required(ckeditor_views.upload), name='ckeditor_upload'),
    url(r'^ckeditor/bbrowse/', login_required(ckeditor_views.browse), name='ckeditor_browse'),

    url(r'^search/', include('search.urls', namespace='search')),
    # partner url
    url(r'^partner/', include('partner.urls')),
    url(r'^partner/', include('microsite.urls')),
    url(r'^linkdin/', include('linkedin.urls')),
    url(r'^register/$', RegistrationApiView.as_view(), name='register'),
    url(r'^login/$', LoginApiView.as_view(), name='login'),
    url(r'^logout/$', LogoutApiView.as_view(), name='logout'),
    url(r'^dashboard/', include('dashboard.urls', namespace='dashboard')),
    url(r'^autologin/(?P<token>.+)/$', AutoLoginView.as_view(), name='autologin'),
    url(r'^linkedin/login/$',
        LinkedinCallbackView.as_view(), name='linkedin-login'),

    url(r'^api/', include('api.urls', namespace='api')),

    # django-oauth-toolkit
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
) + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
) + static(settings.DOWNLOAD_URL, document_root=settings.DOWNLOAD_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

