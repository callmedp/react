from django.conf.urls import url, include

urlpatterns = [
    url(r'^v1/', include(('cms.api.v1.urls','cms'), namespace='v1')),
]