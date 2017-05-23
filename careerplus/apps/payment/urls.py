from django.conf.urls import url

from .views import PaymentOptionView, ThankYouView

urlpatterns = [
	url(r'^payment-options/$', PaymentOptionView.as_view(),
		name='payment-option'),
	url(r'^thank-you/$', ThankYouView.as_view(), name='thank-you'),
]