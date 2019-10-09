from django.conf.urls import url

urlpatterns = [
    url(r'^api/', include('homepage.api.v1.urls', namespace='v1')),
]