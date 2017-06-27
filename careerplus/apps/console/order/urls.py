from django.conf.urls import url, include
urlpatterns = [
    url(r'^partial/', include('console.order.partials.urls', namespace='partials')),
    url(r'^', include('console.order.pages.urls', namespace='pages')),
]