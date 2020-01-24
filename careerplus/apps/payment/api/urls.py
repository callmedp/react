
# from django.conf.urls import url
from django.urls import re_path

from . import views
app_name = 'payment'
urlpatterns = [
re_path(r'^zest-money/emi-plans/$',
	views.ZestMoneyFetchEMIPlansApi.as_view(), name='zest-money-emi')


]
