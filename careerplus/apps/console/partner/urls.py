from django.conf.urls import url, include
urlpatterns = [
    url(r'^partial/', include('console.partner.partials.urls', namespace='partials')),
    url(r'^', include('console.partner.pages.urls', namespace='pages')),
]