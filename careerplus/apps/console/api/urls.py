from django.conf.urls import url, include
app_name = 'console'
urlpatterns = [
    url(r'^v1/', include('console.api.v1.urls', namespace='v1')),
]