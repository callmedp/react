#python imports

#django imports
from django.conf.urls import url

# local imports

from .views import EmailStatusView, UpdateCartView
#inter app imports

# third party imports
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
        url(r'^email-status/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', EmailStatusView.as_view()),
        url(r'^update/$', UpdateCartView.as_view()),

]
