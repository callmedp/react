from django.conf.urls import url, include
app_name = 'shine'
urlpatterns = [
    url(r'^api/', include('shine.api.urls', namespace='v1')),
]