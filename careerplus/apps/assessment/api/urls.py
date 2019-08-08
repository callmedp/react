from django.conf.urls import url, include
from .views import CategoryApiView,TestApiView



urlpatterns = [

url(r'^get-category-level-products',CategoryApiView.as_view(), name='category-level-product'),
url(r'^get-test/',TestApiView.as_view(), name='get-all-test'),

]