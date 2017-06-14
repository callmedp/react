from django.conf.urls import url

from . import blog_view

urlpatterns = [
    url(r'^blog/tag/$', blog_view.TagListView.as_view(), name='tag-list'),
    url(r'^blog/tag/add/$', blog_view.TagAddViewas_view(), name='tag-add'),
    url(r'^blog/tag/(?P<pk>\d+)/change/$', blog_view.TagUpdateViewas_view(),
        name='tag-update'),
]