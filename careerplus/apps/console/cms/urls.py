# from django.conf.urls import url, include
from django.urls import re_path, include

app_name='console'
urlpatterns = [
    re_path(r'^partial/', include('console.cms.partials.urls', namespace='partials')),
    re_path(r'^', include('console.cms.pages.urls', namespace='pages')),
]