# from django.conf.urls import url
from django.urls import re_path
from . import views

app_name = 'console'
urlpatterns = [


    re_path(r'^user-query-action/$', views.UserQueryActionView.as_view(),
        name='user-query-action'),
    re_path(r'^download-hr-query/$', views.DownloadHrQueryView.as_view(), name='download-hr-query'),
    re_path(r'^(?P<query_listing>[-\w]+)/$', views.UserQueryView.as_view(), name='user-query'),

    # re_path(r'^cms-leads/$', views.CMSUserQueryView.as_view(),
    #     name='cms-query'),
    #
    # re_path(r'^skill-leads/$', views.SkillQueryView.as_view(),
    #     name='skill-query'),
    #
    # re_path(r'^course-leads/$', views.CourseQueryView.as_view(),
    #     name='course-query'),
    #
    # re_path(r'^service-leads/$', views.ServiceQueryView.as_view(),
    #     name='service-query'),
    #
    # re_path(r'^human-resource-leads/$', views.HumanResourceQueryView.as_view(),
    #     name='human-resource-query'),


]
