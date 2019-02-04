from django.conf.urls import url

#internal imports
from .views import (UserListCreateApiView, UserRetrieveUpdateApiView)
#third party imports
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^users/(?P<pk>\d+)/$', UserRetrieveUpdateApiView.as_view()),
    url(r'^users/$', UserListCreateApiView.as_view()),
]