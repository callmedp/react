from django.conf.urls import url, include

#internal imports
from .views import UploadResumeShine

#third party imports
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^upload-to-shine/$', UploadResumeShine.as_view()),
]