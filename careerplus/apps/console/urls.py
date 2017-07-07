from django.conf.urls import url
from .views import ConsoleLoginView, ConsoleDashboardView, ConsoleLogoutView
from . import shop_view, vendor_view, blog_view, order_view
from geolocation import adminviews

urlpatterns = [
    url(r'^$', ConsoleDashboardView.as_view(), name='dashboard'),
    url(r'^login/$', ConsoleLoginView.as_view(), name='login'),
    url(r'^logout/$', ConsoleLogoutView.as_view(), name='logout'),
]


urlpatterns += [
    url(r'^screenproduct/list/$',
        vendor_view.ListScreenProductView.as_view(), name='screenproduct-list'),
    url(r'^screenproduct/add/$',
        vendor_view.AddScreenProductView.as_view(), name='screenproduct-add'),
    url(r'^screenproduct/change/(?P<pk>[\d]+)/$',
        vendor_view.ChangeScreenProductView.as_view(), name='screenproduct-change'),
    
    url(r'^screenfaq/list/$',
        vendor_view.ListScreenFaqView.as_view(), name='screenfaq-list'),
        
    url(r'^screenchapter/list/$',
        vendor_view.ListScreenChapterView.as_view(), name='screenchapter-list'),

]

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
    url(r'^product/change/(?P<pk>[\d]+)/$',
        shop_view.ChangeProductView.as_view(), name='product-change'),
    url(r'^product/structurechange/(?P<pk>[\d]+)/$',
        shop_view.ChangeProductStructureView.as_view(),
        name='productstructure-change'),
    url(r'^product/pricechange/(?P<pk>[\d]+)/$',
        shop_view.ChangeProductPriceView.as_view(),
        name='productprice-change'),
    url(r'^product/childchange/(?P<pk>[\d]+)/$',
        shop_view.ChangeProductChildView.as_view(),
        name='productchild-change'),
    url(r'^product/varschange/(?P<pk>[\d]+)/$',
        shop_view.ChangeProductVariationView.as_view(),
        name='productvariation-change'),


    url(r'^faq/add/$',
        shop_view.AddFaqView.as_view(), name='faquestion-add'),
    url(r'^faq/moderation-list/$',
        shop_view.ListModerationFaqView.as_view(), name='mfaquestion-list'),
    url(r'^faq/change/(?P<pk>[\d]+)/$',
        shop_view.ChangeFaqView.as_view(), name='faquestion-change'),
    url(r'^faq/moderate/(?P<pk>[\d]+)/$',
        shop_view.ModerateFaqView.as_view(), name='faquestion-moderate'),
        

    url(r'^chapter/add/$',
        shop_view.AddChapterView.as_view(), name='chapter-add'),
    url(r'^chapter/moderation-list/$',
        shop_view.ListModerationChapterView.as_view(), name='mchapter-list'),
    url(r'^chapter/change/(?P<pk>[\d]+)/$',
        shop_view.ChangeChapterView.as_view(), name='chapter-change'),
    url(r'^chapter/moderate/(?P<pk>[\d]+)/$',
        shop_view.ModerateChapterView.as_view(), name='chapter-moderate'),
        

    url(r'^keyword/add/$',
        shop_view.AddKeywordView.as_view(), name='keyword-add'),
    url(r'^keyword/list/$',
        shop_view.ListKeywordView.as_view(), name='keyword-list'),
    url(r'^keyword/change/(?P<pk>[\d]+)/$',
        shop_view.ChangeKeywordView.as_view(), name='keyword-change'),
    

    url(r'^attribute/add/$',
        shop_view.AddAttributeView.as_view(), name='attribute-add'),
    url(r'^attribute/list/$',
        shop_view.ListAttributeView.as_view(),
        name='attribute-list'),
    url(r'^attribute/change/(?P<pk>[\d]+)/$',
        shop_view.ChangeAttributeView.as_view(), name='attribute-change'),
    

    url(r'^attributeoption/add/$',
        shop_view.AddAttributeOptionView.as_view(),
        name='attributeoption-add'),
    url(r'^attributeoption/list/$',
        shop_view.ListAttributeOptionGroupView.as_view(),
        name='attributeoption-list'),

]


urlpatterns += [
    url(r'^blog/tag/$',
        blog_view.TagListView.as_view(), name='blog-tag-list'),
    url(r'^blog/tag/add/$',
        blog_view.TagAddView.as_view(), name='blog-tag-add'),
    url(r'^blog/tag/(?P<pk>\d+)/change/$', blog_view.TagUpdateView.as_view(),
        name='blog-tag-update'),

    url(r'^blog/category/$', blog_view.CategoryListView.as_view(),
        name='blog-category-list'),
    url(r'^blog/category/add/$', blog_view.CategoryAddView.as_view(),
        name='blog-category-add'),
    url(r'^blog/category/(?P<pk>\d+)/change/$',
        blog_view.CategoryUpdateView.as_view(), name='blog-category-update'),

    url(r'^blog/article/$', blog_view.ArticleListView.as_view(),
        name='blog-article-list'),
    url(r'^blog/article/add/$', blog_view.ArticleAddView.as_view(),
        name='blog-article-add'),
    url(r'^blog/article/(?P<pk>\d+)/change/$',
        blog_view.ArticleUpdateView.as_view(), name='blog-article-update'),

    url(r'^blog/comment/comment-to-moderate/$',
        blog_view.CommentModerateListView.as_view(),
        name='blog-comment-to-moderate'),
    url(r'^blog/comment/(?P<pk>\d+)/change/$',
        blog_view.CommentModerateView.as_view(),
        name='blog-comment-moderate-update'),
]



urlpatterns += [
    url(r'^geolocation/country/$',
        adminviews.CountryListView.as_view(), name='geo-country'),

    url(r'^geolocation/country/(?P<pk>\d+)/change/$',
        adminviews.CountryUpdateView.as_view(), name='geo-country-update'),
]


urlpatterns += [
    url(r'^queue/orders/$',
        order_view.OrderListView.as_view(), name='queue-order'),
    url(r'^queue/welcomecall/$',
        order_view.WelcomeCallVeiw.as_view(), name='queue-welcome'),
    url(r'^queue/midout/$',
        order_view.MidOutQueueView.as_view(), name='queue-midout'),
    url(r'^queue/inbox/$',
        order_view.InboxQueueVeiw.as_view(), name='queue-inbox'),

    url(r'^queue/approval/$',
        order_view.ApprovalQueueVeiw.as_view(), name='queue-approval'),

    url(r'^queue/approved/$',
        order_view.ApprovedQueueVeiw.as_view(), name='queue-approved'),

    url(r'^queue/rejectedbyadmin/$',
        order_view.RejectedByAdminQueue.as_view(), name='queue-rejectedbyadmin'),

    url(r'^queue/rejectedbycandidate/$',
        order_view.RejectedByCandidateQueue.as_view(),
        name='queue-rejectedbycandidate'),

    url(r'^queue/allocated/$',
        order_view.AllocatedQueueVeiw.as_view(), name='queue-allocated'),

    url(r'^queue/closed/orderitems/$',
        order_view.ClosedOrderItemQueueVeiw.as_view(), name='queue-closed-orderitems'),

    url(r'^queue/orderitem/(?P<pk>\d+)/detail/$',
        order_view.OrderItemDetailVeiw.as_view(), name='order-item-detail'),

    url(r'^queue/order/(?P<pk>\d+)/details/$',
        order_view.OrderDetailVeiw.as_view(), name='order-detail'),

    url(r'^queue/orderitem/downloadascsv/$',
        order_view.ActionOrderItemView.as_view(),
        name='action-orderitem-view'),
]