# from django.conf.urls import url
from django.urls import re_path

from coupon.views import CouponRedeemView, CouponRemoveView
from wallet.views import WalletRedeemView, WalletRemoveView

from .views import CartView, AddToCartView, RemoveFromCartView,\
    PaymentLoginView, PaymentShippingView, PaymentSummaryView,\
    UpdateDeliveryType,GuestCouponApply

from . import mobile_view

app_name = 'cart'
urlpatterns = [
    # re_path(r'^$', CartView.as_view(), name='cart-product-list'),
    re_path(r'^add-to-cart/$', AddToCartView.as_view(), name='add-to-cart'),
    re_path(r'^remove-from-cart/$', RemoveFromCartView.as_view(), name='remove-form-cart'),
    re_path(r'^update-deliverytype/$', UpdateDeliveryType.as_view(), name='update-deliverytype'),

    re_path(r'^payment-login/$', PaymentLoginView.as_view(), name='payment-login'),
    # re_path(r'^payment-shipping/$', PaymentShippingView.as_view(), name='payment-shipping'),
    re_path(r'^payment-summary/$', PaymentSummaryView.as_view(), name='payment-summary'),

    re_path(r'^applycoupon/$', CouponRedeemView.as_view(), name='coupon-apply'),
    re_path(r'^removecoupon/$', CouponRemoveView.as_view(), name='coupon-remove'),

    re_path(r'^applypoint/$', WalletRedeemView.as_view(), name='wallet-apply'),
    re_path(r'^removepoint/$', WalletRemoveView.as_view(), name='wallet-remove'),

    re_path(r'^guest-coupon-apply/$',GuestCouponApply.as_view(),name='guest-coupon-apply'),



    # mobile
    re_path(r'^mobile/remove-from-cart/$',
        mobile_view.RemoveFromCartMobileView.as_view(),
        name='remove-form-cart-mobile'),
]