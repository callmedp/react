from django.conf.urls import url, include


app_name = "cms"
urlpatterns = [
    url(r'^v1/', include('cms.api.v1.urls', namespace='v1')),
]