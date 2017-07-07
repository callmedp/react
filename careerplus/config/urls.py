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
from filebrowser.sites import site
from django.conf.urls.static import static

from users.views import (DashboardView,
    RegistrationApiView, LoginApiView, LogoutApiView)
from homepage.views import HomePageView
from linkedin.views import AutoLoginView
from shop.views import ProductDetailView

urlpatterns = []

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
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomePageView.as_view(), name='homepage'),
    url(r'^console/', include('console.urls', namespace='console')),
    url(r'^shop/', include('shop.urls', namespace='shop')),
    url(r'^user/', include('users.urls', namespace='users')),
    url(r'^cms/', include('cms.urls', namespace='cms')),
    url(r'^skillpage/', include('skillpage.urls', namespace='skillpage')),
    url(r'^article/', include('blog.urls', namespace='blog')),
    url(r'^shop/', include('shop.urls', namespace='shop')),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^payment/', include('payment.urls', namespace='payment')),
    url(r'^ajax/', include('ajax.urls', namespace='ajax')),
    url(r'^design/', include('design.urls', namespace='design')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    # partner url
    url(r'^partner/', include('microsite.urls')),
    url(r'^linkdin/', include('linkedin.urls')),
    url(r'^register/$', RegistrationApiView.as_view(), name='register'),
    url(r'^login/$', LoginApiView.as_view(), name='login'),
    # url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^logout/$', LogoutApiView.as_view(), name='logout'),
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^autologin/(?P<token>.+)/$', AutoLoginView.as_view(), name='autologin'),
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
