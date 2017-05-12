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
    url(r'^categoryrelationship/list/$',
        shop_view.ListCategoryRelationView.as_view(),
        name='category-relation-list'),
    url(r'^category/change/(?P<pk>[\d]+)/$',
        shop_view.ChangeCategoryView.as_view(), name='category-change'),
    
    url(r'^product/add/$',
        shop_view.AddProductView.as_view(), name='product-add'),

    url(r'^faq/add/$',
        shop_view.AddFaqView.as_view(), name='faquestion-add'),
    url(r'^faq/list/$',
        shop_view.ListFaqView.as_view(), name='faquestion-list'),

    url(r'^chapter/add/$',
        shop_view.AddChapterView.as_view(), name='chapter-add'),
    url(r'^chapter/list/$',
        shop_view.ListChapterView.as_view(), name='chapter-list'),

    url(r'^keyword/add/$',
        shop_view.AddKeywordView.as_view(), name='keyword-add'),
    url(r'^keyword/list/$',
        shop_view.ListKeywordView.as_view(), name='keyword-list'),

    url(r'^attribute/add/$',
        shop_view.AddAttributeView.as_view(), name='attribute-add'),
    url(r'^attribute/list/$',
        shop_view.ListAttributeView.as_view(),
        name='attribute-list'),

    url(r'^attributeoption/add/$',
        shop_view.AddAttributeOptionView.as_view(),
        name='attributeoption-add'),
    url(r'^attributeoption/list/$',
        shop_view.ListAttributeOptionGroupView.as_view(),
        name='attributeoption-list'),

]
