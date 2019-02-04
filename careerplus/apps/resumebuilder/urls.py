#  django imports
from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/', include('resumebuilder.api.urls', namespace='api'))
]
