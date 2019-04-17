#python imports

#django imports
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

#local imports
from .ccavenue import Ccavenue
from .mobikwik import MobikwikRequestView, MobikwikResponseView
from .views import PaymentOptionView, ThankYouView, PaymentOopsView,\
EPayLaterRequestView, EPayLaterResponseView

#inter app imports

#third party imports

urlpatterns = [
    url(r'^payment-options/$', PaymentOptionView.as_view(),
        name='payment-option'),
    url(r'^thank-you/$', ThankYouView.as_view(), name='thank-you'),

    url(r'^ccavenue/response/(?P<pgstatus>success|cancel)/$', csrf_exempt(Ccavenue.as_view()), name='ccavenue_response'),
    url(r'^ccavenue/request/(?P<cart_id>[-\w]+)/(?P<paytype>[-\w]+)/$',
        csrf_exempt(Ccavenue.as_view()), name='ccavenue_request'),

    url(r'^epaylater/request/(?P<cart_id>[-\w]+)/$',
        EPayLaterRequestView.as_view(), name="epaylater-request"),

    url(r'^epaylater/response/(?P<cart_id>[-\w]+)/$',
        csrf_exempt(EPayLaterResponseView.as_view()), name="epaylater-response"),

    url(r'^oops/$', PaymentOopsView.as_view(), name='payment_oops'),

    # url("^mobikwik/request?$", MobikwikRequestView.as_view(), name='mobikwik_request'),
    # url("^mobikwik/response/$", MobikwikResponseView.as_view(), name='mobikwik_response'),
    # url("^dipifrs/application/$",
    #     PaymentPageDipIfrsView.as_view(), name='PaymentPageDipIfrsView'),
]