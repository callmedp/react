from django.urls import re_path, include
app_name='userintent'

urlpatterns = [
    re_path(r'^v1/', include('userintent.api.v1.urls', namespace='userintent-api')),
]