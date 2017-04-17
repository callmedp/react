from django.conf.urls import url

from .views import BlogLandingPageView, BlogLandingAjaxView
from .adminview import TagAddFormView, CategoryAddFormView, BlogAddFormView,\
    TagListView, TagUpdateView, CategoryListView, CategoryUpdateView,\
    BlogListView, BlogUpdateView

urlpatterns = [
    url(r'^$', BlogLandingPageView.as_view(), name='blog-landing'),
    url(r'^category-wise-loading/$', BlogLandingAjaxView.as_view(),
    	name='blog-landing-load'),

    url(r'^admin/tag-add/$', TagAddFormView.as_view(),
    	name='blog-tag-add'),

    url(r'^admin/tags/$', TagListView.as_view(),
    	name='blog-tag-list'),

    url(r'^admin/tags/(?P<pk>\d+)/change/$', TagUpdateView.as_view(),
    	name='blog-tag-update'),

    url(r'^admin/category-add/$', CategoryAddFormView.as_view(),
    	name='blog-category-add'),

    url(r'^admin/categories/$', CategoryListView.as_view(),
    	name='blog-category-list'),

    url(r'^admin/categories/(?P<pk>\d+)/change/$', CategoryUpdateView.as_view(),
    	name='blog-category-update'),

    url(r'^admin/article-add/$', BlogAddFormView.as_view(),
    	name='blog-article-add'),

    url(r'^admin/articles/$', BlogListView.as_view(),
    	name='blog-article-list'),

    url(r'^admin/articles/(?P<pk>\d+)/change/$', BlogUpdateView.as_view(),
    	name='blog-article-update'),
]
