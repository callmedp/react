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
app_name = 'shop'
urlpatterns = [
    url(r'^reviews/(?P<product_pk>[\w-]+)/$',
        views.ProductReviewListView.as_view(), name='product-review'),

    url(r'^product/content-by-ajax/$',
        views.ProductDetailContent.as_view(), name='product-detail-ajax'),

    url(r'^reviews/(?P<product_pk>[\w-]+)/edit/$',
        views.ProductReviewEditView.as_view(), name='product-review-edit'),

    url(r'^reviews/product/create/$',
        views.ProductReviewCreateView.as_view(), name='product-review-create'),

    url(r'^product/(?P<skill_name>[\w|\W]+)/$',
        views.SkillToProductRedirectView.as_view(), name="skill-to-product-redirect")

    # url(r'^crm/lead/$',
    #     views.LeadView.as_view(), name='crm-lead'),
]
