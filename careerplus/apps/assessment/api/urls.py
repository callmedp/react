# from django.conf.urls import url, include
from django.urls import re_path, include
from .views import CategoryApiView,TestApiView


app_name='assessment'
urlpatterns = [

re_path(r'^get-category-level-products',CategoryApiView.as_view(), name='category-level-product'),
re_path(r'^get-test/',TestApiView.as_view(), name='get-all-test'),

]