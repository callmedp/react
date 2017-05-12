from django.conf.urls import url
from .views import CartView, AddToCartView


urlpatterns = [
	url(r'^$', CartView.as_view(), name='cart-product-list'),
	url(r'^add-to-cart/$', AddToCartView.as_view(), name='add-to-cart'),

]