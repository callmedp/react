from django.conf.urls import url, include

app_name = "users"
urlpatterns = [
    url(r'^v1/', include('users.api.v1.urls', namespace='v1')),
]