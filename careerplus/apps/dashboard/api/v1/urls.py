from django.urls import re_path
from . import views

app_name = "dashboard"

urlpatterns = [
    re_path(r'^my-orders/$', views.DashboardMyorderApi.as_view(), name='my-orders'),
    re_path(r'^my-courses/$', views.MyCoursesApi.as_view(), name='my-courses'),
    re_path(r'^my-services/$', views.MyServicesApi.as_view(), name='my-services'),
    re_path(r'^my-wallet/$', views.DashboardMyWalletAPI.as_view(), name='my-wallet'),
    re_path(r'^review/$', views.DashboardReviewApi.as_view(),name='dashboard-feedback'),
    re_path(r'^pending-resume_items/$', views.DashboardPendingResumeItemsApi.as_view(),name='pending-resume-item'),
    re_path(r'^view-order-details/$', views.ViewOrderDetailsApi.as_view(), name='my-services'),
]
