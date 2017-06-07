from django.conf.urls import url

from .views import SkillPageView, SkillQueryLead
from .adminview import SkillAddFormView, SkillListView, SkillUpdateView

urlpatterns = [
    url(r'^skill-page-listing/(?P<slug>[-\w]+)/(?P<pk>\d+)/$', SkillPageView.as_view(), name='skill-page-listing'),
    url(r'^skill-query-lead/$', SkillQueryLead.as_view(), name='skill-query-lead'),
    url(r'^admin/skill-add/$', SkillAddFormView.as_view(),
    	name='skill-add'),
    url(r'^admin/skill-list/$', SkillListView.as_view(),
    	name='skill-list'),
    url(r'^admin/skill/(?P<pk>\d+)/change/$', SkillUpdateView.as_view(),
    	name='skill-update'),
]