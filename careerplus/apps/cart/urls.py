from django.conf.urls import url
from .views import CartView, AddToCartView, RemoveFromCartView,\
	PaymentLoginView, PaymentShippingView, PaymentSummaryView
from coupon.views import CouponRedeemView, CouponRemoveView
from wallet.views import WalletRedeemView, WalletRemoveView


urlpatterns = [
	url(r'^$', CartView.as_view(), name='cart-product-list'),
	url(r'^add-to-cart/$', AddToCartView.as_view(), name='add-to-cart'),
	url(r'^remove-from-cart/$', RemoveFromCartView.as_view(), name='remove-form-cart'),

	url(r'^payment-login/$', PaymentLoginView.as_view(), name='payment-login'),
	url(r'^payment-shipping/$', PaymentShippingView.as_view(), name='payment-shipping'),
	url(r'^payment-summary/$', PaymentSummaryView.as_view(), name='payment-summary'),

	url(r'^applycoupon/$', CouponRedeemView.as_view(), name='coupon-apply'),
	url(r'^removecoupon/$', CouponRemoveView.as_view(), name='coupon-remove'),
	
	url(r'^applypoint/$', WalletRedeemView.as_view(), name='wallet-apply'),
	url(r'^removepoint/$', WalletRemoveView.as_view(), name='wallet-remove'),
			
]