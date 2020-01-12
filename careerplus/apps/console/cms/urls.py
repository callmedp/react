from django.conf.urls import url, include

app_name='console'
urlpatterns = [
    url(r'^partial/', include('console.cms.partials.urls', namespace='partials')),
    url(r'^', include('console.cms.pages.urls', namespace='pages')),
]