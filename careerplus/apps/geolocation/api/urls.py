from django.conf.urls import url, include
app_name= 'geolocation'
urlpatterns = [
    url(r'^v1/', include('geolocation.api.v1.urls', namespace='v1')),
]