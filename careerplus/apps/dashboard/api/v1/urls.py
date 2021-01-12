from django.urls import re_path
from . import views

app_name = "dashboard"

urlpatterns = [
    re_path(r'^my-orders/$', views.DashboardMyorderApi.as_view(), name='my-orders'),
    re_path(r'^my-courses/$', views.MyCoursesApi.as_view(), name='my-courses'),
    re_path(r'^my-services/$', views.MyServicesApi.as_view(), name='my-services'),
    re_path(r'^my-wallet/$', views.DashboardMyWalletAPI.as_view(), name='my-wallet'),

]
