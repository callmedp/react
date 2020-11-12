# from django.conf.urls import url
from django.urls import re_path
from django.conf import settings

from .views import LoadMoreApiView, SkillPageAbout, CourseComponentView, DomainJobsView
app_name='skillpage'
urlpatterns = [
    re_path(r'^v1/load-more/$',
        LoadMoreApiView.as_view(),
        name='load-more'),
    re_path(r'^v1/about/$',SkillPageAbout.as_view(),name='skill-about'),
    re_path(r'^v1/courses/$',CourseComponentView.as_view(),name='courses-tray'),
    re_path(r'^v1/domain-jobs/$',DomainJobsView.as_view(),name='domain-jobs')
]