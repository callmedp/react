from django.urls import re_path,include


app_name = 'wallet'


urlpatterns = [
    re_path('^',include('wallet.api.urls')),

]