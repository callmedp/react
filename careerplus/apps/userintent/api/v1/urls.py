from django.urls import re_path
from . import views
app_name = "userintent"

urlpatterns = [
    re_path(r'^course-recommendation/$',views.CourseRecommendationAPI.as_view(), name='course-recommendation'),
    re_path(r'^service-recommendation/$',views.ServiceRecommendationAPI.as_view(), name='service-recommendation'),
    re_path(r'^jobs/$',views.JobsSearchAPI.as_view(), name='search-jobs'),
]