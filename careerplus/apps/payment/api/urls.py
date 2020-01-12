
from django.conf.urls import url

from . import views
app_name = 'payment'
urlpatterns = [
url(r'^zest-money/emi-plans/$',
	views.ZestMoneyFetchEMIPlansApi.as_view(), name='zest-money-emi')


]
