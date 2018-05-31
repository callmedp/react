from django.conf.urls import url

# from .adminview import ProductAddFormView, ProductListView, ProductUpdateView

# urlpatterns = [
#     url(r'^admin/product-add/$', ProductAddFormView.as_view(),
#     	name='product-add'),
#     url(r'^admin/product-list/$', ProductListView.as_view(),
#         name='product-list'),
    
#     url(r'^admin/product/(?P<pk>\d+)/change/$', ProductUpdateView.as_view(),
#     	name='product-update'),
# ]

from . import views

urlpatterns = [
    url(r'^reviews/(?P<product_pk>[\w-]+)/$',
        views.ProductReviewListView.as_view(), name='product-review'),

    url(r'^product/content-by-ajax/$',
        views.ProductDetailContent.as_view(), name='product-detail-ajax'),

    # url(r'^crm/lead/$',
    #     views.LeadView.as_view(), name='crm-lead'),
]
