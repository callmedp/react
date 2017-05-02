from django.conf.urls import url, include

urlpatterns = [
    url(r'^cms/', include('console.cms.urls', namespace='cms')),
]
