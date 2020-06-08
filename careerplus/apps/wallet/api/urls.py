from django.urls import re_path,include

from .views import  WalletTxnsHistory


app_name = 'wallet'


urlpatterns = [
    re_path(r'^v1/wallettxn/$',WalletTxnsHistory.as_view()),
]