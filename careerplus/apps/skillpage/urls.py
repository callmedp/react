from django.conf.urls import url

from .views import SkillPageView, SkillQueryLead

urlpatterns = [
    url(r'^skill-page-listing/(?P<slug>[-\w]+)/$', SkillPageView.as_view(), name='skill-page-listing'),
    url(r'^skill-query-lead/$', SkillQueryLead.as_view(), name='skill-query-lead'),
]