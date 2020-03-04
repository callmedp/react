from django.urls import re_path

from . import blog_view
app_name = 'console'
urlpatterns = [
    re_path(r'^blog/tag/$', blog_view.TagListView.as_view(), name='tag-list'),
    re_path(r'^blog/tag/add/$', blog_view.TagAddViewas_view(), name='tag-add'),
    re_path(r'^blog/tag/(?P<pk>\d+)/change/$', blog_view.TagUpdateViewas_view(),
        name='tag-update'),
]