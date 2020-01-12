from django.conf.urls import url, include
app_name='homepage'
urlpatterns = [
    url(r'^v1/', include('homepage.api.v1.urls', namespace='v1')),
]