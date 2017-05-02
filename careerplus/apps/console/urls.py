from django.conf.urls import url
from .views import ConsoleLoginView, ConsoleDashboardView, ConsoleLogoutView

urlpatterns = [
    url(r'^$', ConsoleDashboardView.as_view(), name='dashboard'),
    url(r'^login/$', ConsoleLoginView.as_view(), name='login'),
    url(r'^logout/$', ConsoleLogoutView.as_view(), name='logout'),
]


from . import shop_view

urlpatterns += [
    url(r'^category/add/$',
        shop_view.AddCategoryView.as_view(), name='category-add'),
    url(r'^category/list/$',
        shop_view.ListCategoryView.as_view(), name='category-list'),
    url(r'^category/change/(?P<pk>[\d]+)/$',
        shop_view.ChangeCategoryView.as_view(), name='category-change'),
    url(r'^categoryrelationship/add/$',
        shop_view.AddCategoryRelationView.as_view(),
        name='category-relation-add'),
    url(r'^categoryrelationship/list/$',
        shop_view.ListCategoryRelationView.as_view(),
        name='category-relation-list'),
    url(r'^categoryrelationship/change/(?P<pk>[\d]+)/$',
        shop_view.ChangeCategoryRelationView.as_view(),
        name='category-relation-change'),
    url(r'^categoryrelationship/remove/(?P<pk>[\d]+)/$',
        shop_view.RemoveCategoryRelationView.as_view(),
        name='category-relation-remove'),
]
