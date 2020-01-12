from django.conf.urls import url, include
app_name = 'geolocation'
urlpatterns = [
    url(r'^api/', include('geolocation.api.urls', namespace='api')),
]
