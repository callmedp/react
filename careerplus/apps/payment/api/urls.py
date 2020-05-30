
# from django.conf.urls import url
from django.urls import re_path
from . import views

app_name = 'payment'

urlpatterns = [
	
	re_path(r'^zest-money/emi-plans/$', views.ZestMoneyFetchEMIPlansApi.as_view(), name='zest-money-emi'),

	re_path(r'^payu/request/$', views.ResumeShinePayuRequestAPIView.as_view()),

	re_path(r'^payu/resume-response/(?P<type>success|cancel|failure)/$', views.ResumeShinePayuRequestAPIView.as_view()),

	re_path(r'^ccavenue/request/(?P<cart_id>[-\w]+)/(?P<paytype>[-\w]+)/$',
			(views.Ccavenue.as_view())),
	re_path(r'^epaylater/request/(?P<cart_id>[-\w]+)/$',
			views.EPayLaterRequestView.as_view(), name="epaylater-request"),


]
