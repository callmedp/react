from django.conf.urls import url

from .views import CounsellingSubmit

urlpatterns = [
    url(r'^counsellingform/(?P<order_item>[-\w]+)/$',
        CounsellingSubmit.as_view(), name='counselling-form'),    
]
