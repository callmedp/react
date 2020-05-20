#python imports

#django imports
# from django.conf.urls import url
from django.urls import re_path

# local imports

from .views import EmailStatusView, CartRetrieveUpdateView,  CartCountView, AddToCartApiView
#inter app imports

# third party imports
from rest_framework import routers

router = routers.DefaultRouter()
app_name='cart'
urlpatterns = [
        re_path(r'^email-status/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', EmailStatusView.as_view()),
        re_path(r'^(?P<pk>\d+)/$', CartRetrieveUpdateView.as_view()),
        re_path(r'^count/$', CartCountView.as_view()),
        re_path(r'^add/$', AddToCartApiView.as_view())


]
