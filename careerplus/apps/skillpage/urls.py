# from django.conf.urls import url, include
from django.urls import re_path, include

from .views import (
    SkillPageView)
from search.views import FuncAreaPageView

# from .adminview import SkillAddFormView, SkillListView, SkillUpdateView

app_name = 'skillpage'

urlpatterns = [
    re_path(r'^(?P<fa_slug>[-\w]+)/(?P<pk>\d+)/$',
        FuncAreaPageView.as_view(), name='func_area_results'),
    re_path(r'^(?P<fa_slug>[-\w]+)/(?P<skill_slug>[-\w]+)/(?P<pk>\d+)/$',
        SkillPageView.as_view(), name='skill-page-listing'),
    re_path(r'^api/',include('skillpage.api.v1.urls',
                          namespace='skillpage-api')),

    ## NOT IN USE
    # re_path(r'^admin/skill-add/$', SkillAddFormView.as_view(),
    # 	name='skill-add'),
    # re_path(r'^admin/skill-list/$', SkillListView.as_view(),
    # 	name='skill-list'),
    # re_path(r'^admin/skill/(?P<pk>\d+)/change/$', SkillUpdateView.as_view(),
    # 	name='skill-update'),
]
