# django imports
from django.conf.urls import url, include

urlpatterns = [
    url(r'^v1/', include('resumebuilder.api.v1.urls', namespace='v1')),
]
