
from django.conf.urls import url

from . import views

urlpatterns = [
url(r'^zest-money/emi-plans/$',
	views.ZestMoneyFetchEMIPlansApi.as_view(), name='zest-money-emi')


]
