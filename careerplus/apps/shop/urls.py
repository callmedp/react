from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^reviews/(?P<product_pk>[\w-]+)/$',
        views.ProductReviewListView.as_view(), name='product-review'),
]
