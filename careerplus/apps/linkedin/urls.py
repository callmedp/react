from django.conf.urls import url

from .views import CounsellingSubmit, LinkedinDraftView

urlpatterns = [
    url(r'^counsellingform/(?P<order_item>[-\w]+)/$',
        CounsellingSubmit.as_view(), name='counselling-form'),

    url(r'^linkedin-draft/(?P<order_item>[-\w]+)/(?P<op_id>[-\w]+)/$',
        LinkedinDraftView.as_view(), name='linkedin-draft'),    
]
