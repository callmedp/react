from django.conf.urls import url
from .views import ProductListView


urlpatterns = [
    url(r'^products/$', ProductListView.as_view()),
]
