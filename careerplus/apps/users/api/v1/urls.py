from django.conf.urls import url

#internal imports
from .views import GetUsersView

#third party imports
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^get-users/$', GetUsersView.as_view()),
]