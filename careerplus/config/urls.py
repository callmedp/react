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
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from shop.views import ProductDetailView
urlpatterns = []

urlpatterns += [
    url(r'^courses/(?P<cat_slug>[\w-])/(?P<prd_slug>[\w-])/$',
        ProductDetailView.as_view(), name='course-detail'),
    url(r'^writing-services/(?P<cat_slug>[\w-])/(?P<prd_slug>[\w-])/$',
        ProductDetailView.as_view(), name='resume-detail'),
    url(r'^job-assistance/(?P<cat_slug>[\w-])/(?P<prd_slug>[\w-])/$',
        ProductDetailView.as_view(), name='job-assist-detail'),
]

urlpatterns += [

    url(r'^admin/', include(admin.site.urls)),
    url(r'^console/', include('console.urls', namespace='console')),
    url(r'^design/', include('design.urls', namespace='design')),

] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
