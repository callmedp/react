from django.conf.urls import url
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^TermAndAgreement/$',
        views.TermsAndAgreementView.as_view(), name='TermAndAgreement')
    ]