from . import views
from django.urls import re_path

urlpatterns = [
    re_path(r'^resume-score-checker/save-data$',
        views.SaveResumeDetailsApiView.as_view(), name='resume-score-checker-save-data'),
    re_path(r'^resume-score-checker/get-score$',
        views.GetResumeScoreApiView.as_view(), name='resume-score-checker-get-score')
]