from django.conf.urls import url, include

from .views import (
    SkillPageView, ServiceDetailPage,
    UniversityPageView)
from search.views import FuncAreaPageView

# from .adminview import SkillAddFormView, SkillListView, SkillUpdateView

urlpatterns = [
    url(r'^(?P<fa_slug>[-\w]+)/(?P<pk>\d+)/$',
        FuncAreaPageView.as_view(), name='func_area_results'),
    url(r'^(?P<fa_slug>[-\w]+)/(?P<skill_slug>[-\w]+)/(?P<pk>\d+)/$',
        SkillPageView.as_view(), name='skill-page-listing'),
    url(r'^api/',include(('skillpage.api.v1.urls','skillpage'),
                          namespace='skillpage-api')),

    ## NOT IN USE
    # url(r'^admin/skill-add/$', SkillAddFormView.as_view(),
    # 	name='skill-add'),
    # url(r'^admin/skill-list/$', SkillListView.as_view(),
    # 	name='skill-list'),
    # url(r'^admin/skill/(?P<pk>\d+)/change/$', SkillUpdateView.as_view(),
    # 	name='skill-update'),
]
