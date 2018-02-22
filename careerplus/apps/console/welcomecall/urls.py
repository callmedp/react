from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^queue/$', views.WelcomeQueueView.as_view(),
        name='wecome-queue'),
]
