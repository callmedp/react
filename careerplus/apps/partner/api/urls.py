from django.conf.urls import url, include
app_name = 'partner'
urlpatterns = [
    url(r'^v1/', include('partner.api.v1.urls', namespace='v1')),
]