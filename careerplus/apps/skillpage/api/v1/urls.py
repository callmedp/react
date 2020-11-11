# from django.conf.urls import url
from django.urls import re_path
from django.conf import settings

from .views import LoadMoreApiView, SkillPageAbout
app_name='skillpage'
urlpatterns = [
    re_path(r'^v1/load-more/$',
        LoadMoreApiView.as_view(),
        name='load-more'),
    re_path(r'^v1/about/$',SkillPageAbout.as_view(),name='skill-about')
]