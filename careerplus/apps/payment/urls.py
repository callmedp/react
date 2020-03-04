#python imports

#django imports
# from django.conf.urls import url,include
from django.urls import re_path,include
from django.views.decorators.csrf import csrf_exempt

#local imports
from .ccavenue import Ccavenue
from .mobikwik import MobikwikRequestView, MobikwikResponseView
from .views import (PaymentOptionView, ThankYouView, PaymentOopsView,\
EPayLaterRequestView, EPayLaterResponseView,ZestMoneyRequestApiView,\
    ZestMoneyResponseView,PayuRequestView,PayUResponseView )


#inter app imports

#third party imports
app_name = 'payment'
urlpatterns = [
    re_path(r'^payment-options/$', PaymentOptionView.as_view(),
        name='payment-option'),
    re_path(r'^thank-you/$', ThankYouView.as_view(), name='thank-you'),

    re_path(r'^ccavenue/response/(?P<pgstatus>success|cancel)/$', csrf_exempt(Ccavenue.as_view()), name='ccavenue_response'),
    re_path(r'^ccavenue/request/(?P<cart_id>[-\w]+)/(?P<paytype>[-\w]+)/$',
        csrf_exempt(Ccavenue.as_view()), name='ccavenue_request'),

    re_path(r'^epaylater/request/(?P<cart_id>[-\w]+)/$',
        EPayLaterRequestView.as_view(), name="epaylater-request"),

    re_path(r'^epaylater/response/(?P<cart_id>[-\w]+)/$',
        csrf_exempt(EPayLaterResponseView.as_view()), name="epaylater-response"),

    re_path(r'^oops/$', PaymentOopsView.as_view(), name='payment_oops'),

    re_path(r'^api/', include('payment.api.urls'), name='payment_api'),

    re_path(r'^zestmoney/request/(?P<cart_id>[-\w]+)/$',
        ZestMoneyRequestApiView.as_view(), name="zestmoney-request"),

    re_path(r'^zest-money/(?P<txn_id>\d+)/callback/$',
         ZestMoneyResponseView.as_view(),name='zestmoney-response'),

    re_path(r'^payu/request/(?P<cart_id>[-\w]+)/$',
        csrf_exempt(PayuRequestView.as_view()), name="payu-request"),

    re_path(r'^payu/response/(?P<type>success|cancel|failure)/$',
        csrf_exempt(PayUResponseView.as_view()), name="payu-response"),

    # re_path("^mobikwik/request?$", MobikwikRequestView.as_view(), name='mobikwik_request'),
    # re_path("^mobikwik/response/$", MobikwikResponseView.as_view(), name='mobikwik_response'),
    # re_path("^dipifrs/application/$",
    #     PaymentPageDipIfrsView.as_view(), name='PaymentPageDipIfrsView'),
]