from django.conf.urls import url, include
from .views import CategoryApiView



urlpatterns = [

url(r'^get-category-level-products',CategoryApiView.as_view(), name='category-level-product'),
]