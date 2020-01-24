# from django.conf.urls import url
from django.urls import re_path

# from .adminview import ProductAddFormView, ProductListView, ProductUpdateView

# urlpatterns = [
#     re_path(r'^admin/product-add/$', ProductAddFormView.as_view(),
#     	name='product-add'),
#     re_path(r'^admin/product-list/$', ProductListView.as_view(),
#         name='product-list'),

#     re_path(r'^admin/product/(?P<pk>\d+)/change/$', ProductUpdateView.as_view(),
#     	name='product-update'),
# ]

from . import views
app_name = 'shop'
urlpatterns = [
    re_path(r'^reviews/(?P<product_pk>[\w-]+)/$',
        views.ProductReviewListView.as_view(), name='product-review'),

    re_path(r'^product/content-by-ajax/$',
        views.ProductDetailContent.as_view(), name='product-detail-ajax'),

    re_path(r'^reviews/(?P<product_pk>[\w-]+)/edit/$',
        views.ProductReviewEditView.as_view(), name='product-review-edit'),

    re_path(r'^reviews/product/create/$',
        views.ProductReviewCreateView.as_view(), name='product-review-create'),

    re_path(r'^product/(?P<skill_name>[\w|\W]+)/$',
        views.SkillToProductRedirectView.as_view(), name="skill-to-product-redirect")

    # re_path(r'^crm/lead/$',
    #     views.LeadView.as_view(), name='crm-lead'),
]
