from django.urls import re_path
from . import views
app_name = "userintent"

urlpatterns = [
    re_path(r'^course-recommendation/$',views.CourseRecommendationAPI.as_view(), name='course-recommendation'),
]