# from django.conf.urls import url
from django.urls import re_path

#internal imports
from .views import GetUsersView

#third party imports
from rest_framework import routers

router = routers.DefaultRouter()
app_name = 'users'
urlpatterns = [
    re_path(r'^get-users/$', GetUsersView.as_view()),

]