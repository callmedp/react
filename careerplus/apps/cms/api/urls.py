from django.urls import re_path, include


app_name = "cms"
urlpatterns = [
    re_path(r'^v1/', include('cms.api.v1.urls', namespace='v1')),
]