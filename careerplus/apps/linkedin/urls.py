from django.conf.urls import url

from .views import CounsellingSubmit

urlpatterns = [
    url(r'^counsellingform/$',
        CounsellingSubmit.as_view(), name='counselling-form'),
]
