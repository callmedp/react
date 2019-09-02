from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/', include('shine.api.urls', namespace='v1')),
]