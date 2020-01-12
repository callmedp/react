from django.conf.urls import url
from . import views

app_name = 'console'
urlpatterns = [


    url(r'^user-query-action/$', views.UserQueryActionView.as_view(),
        name='user-query-action'),
    url(r'^download-hr-query/$', views.DownloadHrQueryView.as_view(), name='download-hr-query'),
    url(r'^(?P<query_listing>[-\w]+)/$', views.UserQueryView.as_view(), name='user-query'),

    # url(r'^cms-leads/$', views.CMSUserQueryView.as_view(),
    #     name='cms-query'),
    #
    # url(r'^skill-leads/$', views.SkillQueryView.as_view(),
    #     name='skill-query'),
    #
    # url(r'^course-leads/$', views.CourseQueryView.as_view(),
    #     name='course-query'),
    #
    # url(r'^service-leads/$', views.ServiceQueryView.as_view(),
    #     name='service-query'),
    #
    # url(r'^human-resource-leads/$', views.HumanResourceQueryView.as_view(),
    #     name='human-resource-query'),


]
