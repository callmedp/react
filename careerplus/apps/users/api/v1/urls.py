from django.conf.urls import url

#internal imports
from .views import GetUsersView

#third party imports
from rest_framework import routers

router = routers.DefaultRouter()
app_name = 'users'
urlpatterns = [
    url(r'^get-users/$', GetUsersView.as_view()),

]