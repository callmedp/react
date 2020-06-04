
# from django.conf.urls import url
from django.urls import re_path
from . import views
from .thankyou import ThankYouAPIView
from django.views.decorators.csrf import csrf_exempt


app_name = 'payment'

urlpatterns = [
    re_path(r'^zest-money/emi-plans/$',
            views.ZestMoneyFetchEMIPlansApi.as_view(), name='zest-money-emi'),

    re_path(r'^payu/request/$', views.ResumeShinePayuRequestAPIView.as_view()),

    re_path(r'^payu/resume-response/(?P<type>success|cancel|failure)/$',
            views.ResumeShinePayuRequestAPIView.as_view()),

    re_path(r'^ccavenue/response/(?P<pgstatus>success|cancel)/$', csrf_exempt(views.Ccavenue.as_view()),
            name='ccavenue_response'),

    re_path(r'^ccavenue/request/(?P<cart_id>[-\w]+)/(?P<paytype>[-\w]+)/$',
            (views.Ccavenue.as_view())),
    re_path(r'^epaylater/request/(?P<cart_id>[-\w]+)/$',
            views.EPayLaterRequestView.as_view(), name="epaylater-request"),

    re_path(r'^zest-money/(?P<txn_id>\d+)/callback/$',
            views.ZestMoneyResponseView.as_view(), name='zestmoney-response'),

    re_path(r'^thankyou/$', ThankYouAPIView.as_view(), name="thank-you"),
]
